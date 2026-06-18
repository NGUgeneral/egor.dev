#!/usr/bin/env python3
"""
Ultra-lightweight static site generator for egor.dev
Converts Markdown content with front-matter to static HTML using Jinja2 templates.
"""

import os
import shutil
import re
from datetime import datetime
from pathlib import Path
import markdown
from jinja2 import Environment, FileSystemLoader

# Configuration
BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
POSTS_DIR = CONTENT_DIR / "posts"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "docs"
LAYOUT_TEMPLATE = "layout.html"

# Ensure paths exist
TEMPLATES_DIR.mkdir(exist_ok=True)
CONTENT_DIR.mkdir(exist_ok=True)
POSTS_DIR.mkdir(exist_ok=True)


def parse_front_matter(content):
    """
    Parse YAML-style front-matter from markdown.
    Expects format:
    ---
    key: value
    key2: value2
    ---
    # Markdown content
    
    Returns: (metadata_dict, markdown_content_string)
    """
    if not content.startswith("---"):
        return {}, content

    # Split on the second --- occurrence
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    front_matter_text = parts[1].strip()
    markdown_content = parts[2].strip()

    # Parse front-matter (simple YAML key: value parsing)
    metadata = {}
    for line in front_matter_text.split("\n"):
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()

    return metadata, markdown_content


def render_markdown(content):
    """Convert markdown to HTML."""
    return markdown.markdown(content, extensions=["fenced_code", "tables", "toc"])


def read_file(path):
    """Read file content."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    """Write file content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def clear_docs_dir():
    """Clear the docs directory completely."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
        print(f"✓ Cleared {OUTPUT_DIR}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def process_post(post_path):
    """
    Process a single post markdown file.
    Returns: {path_slug, metadata, html_content, file_path}
    """
    content = read_file(post_path)
    metadata, markdown_content = parse_front_matter(content)
    html_content = render_markdown(markdown_content)

    # Generate slug from filename (remove .md extension)
    slug = post_path.stem

    return {
        "slug": slug,
        "title": metadata.get("title", slug.replace("-", " ").title()),
        "date": metadata.get("date", ""),
        "excerpt": metadata.get("excerpt", ""),
        "content": html_content,
        "file_path": post_path,
    }


def parse_date(date_str):
    """Parse date string to datetime object for sorting."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return datetime.min


def build_posts_page(posts):
    """Build a dedicated posts listing page at /posts/index.html."""
    if not posts:
        print("⚠ No posts to list.")
        return

    # Build posts list HTML
    posts_list_html = '<ul class="post-list">'
    for post in posts:
        posts_list_html += f'''
    <li class="post-item">
        <div class="post-title">
            <a href="/post/{post["slug"]}/">{post["title"]}</a>
        </div>
        <div class="post-date">{post["date"]}</div>
        <div class="post-excerpt">{post["excerpt"]}</div>
    </li>
'''
    posts_list_html += "</ul>"

    # Render posts page
    posts_page_html = env.get_template(LAYOUT_TEMPLATE).render(
        title="Posts",
        description="A collection of posts about backend engineering, system design, and technical insights.",
        content=f"<h1>Posts</h1>\n{posts_list_html}",
        meta_tags='<meta name="og:type" content="website">',
    )

    output_path = OUTPUT_DIR / "posts" / "index.html"
    write_file(output_path, posts_page_html)
    print(f"✓ Generated posts page: {output_path.relative_to(BASE_DIR)}")


def build_posts():
    """Build all post pages and return sorted list of posts."""
    posts = []

    if not POSTS_DIR.exists():
        print("⚠ No posts directory found.")
        return posts

    # Process all .md files in posts directory
    for post_file in sorted(POSTS_DIR.glob("*.md")):
        post = process_post(post_file)
        posts.append(post)
        print(f"✓ Processed: {post['title']} ({post_file.name})")

    # Sort posts by date (newest first)
    posts.sort(key=lambda p: parse_date(p["date"]), reverse=True)

    # Generate HTML for each post
    for post in posts:
        output_path = OUTPUT_DIR / "post" / post["slug"] / "index.html"

        # Render post page
        post_html = env.get_template(LAYOUT_TEMPLATE).render(
            title=post["title"],
            description=post.get("excerpt", ""),
            content=post["content"],
            meta_tags=f'<meta name="date" content="{post["date"]}">',
        )

        write_file(output_path, post_html)
        print(f"  → Generated: {output_path.relative_to(BASE_DIR)}")

    return posts


def build_home(posts):
    """Build the home page (about.md) without posts list."""
    about_path = CONTENT_DIR / "about.md"

    if not about_path.exists():
        print("⚠ No about.md found. Skipping home page generation.")
        return

    content = read_file(about_path)
    metadata, markdown_content = parse_front_matter(content)
    html_content = render_markdown(markdown_content)

    # Render home page with just about content
    home_html = env.get_template(LAYOUT_TEMPLATE).render(
        title="Home",
        description="Backend engineer, system design enthusiast, and technical writer.",
        content=html_content,
        meta_tags='<meta name="og:type" content="website">',
    )

    output_path = OUTPUT_DIR / "index.html"
    write_file(output_path, home_html)
    print(f"✓ Generated home page: {output_path.relative_to(BASE_DIR)}")


def create_robots_txt():
    """Create a robots.txt file for SEO."""
    robots_content = """User-agent: *
Allow: /

Sitemap: https://egor.dev/sitemap.xml
"""
    write_file(OUTPUT_DIR / "robots.txt", robots_content)
    print(f"✓ Generated: robots.txt")


def create_gitkeep():
    """Create .gitkeep to ensure docs directory is tracked by git."""
    # Create an empty .gitkeep file
    gitkeep_path = OUTPUT_DIR / ".gitkeep"
    gitkeep_path.touch()


def main():
    """Main build process."""
    print("\n🔨 Building static site...\n")

    # Step 1: Clear output directory
    clear_docs_dir()

    # Step 2: Setup Jinja2 environment
    global env
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    # Step 3: Build posts
    posts = build_posts()
    print()

    # Step 4: Build dedicated posts listing page
    build_posts_page(posts)

    # Step 5: Build home page (without posts list)
    build_home(posts)

    # Step 6: Create SEO files
    create_robots_txt()
    create_gitkeep()

    print(f"\n✅ Build complete! Output: {OUTPUT_DIR}\n")
    print(f"Generated files:")
    print(f"  - Home page: /")
    print(f"  - Posts listing: /posts/")
    print(f"  - {len(posts)} post(s) at /post/{{slug}}/")
    print()


if __name__ == "__main__":
    main()
