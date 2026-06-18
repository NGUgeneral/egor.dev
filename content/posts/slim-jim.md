---
title: Slim Jim – Lightweight HTML to PDF Conversion
date: 2026-06-16
excerpt: Engineering a pragmatic, low-footprint HTML-to-PDF serverless microservice using strategic dependencies and clean architecture.
---

# Slim Jim – Lightweight HTML to PDF Conversion

![Slim Jim Architecture](/assets/Slim%20Jim.jpg)

Yet another HTML to PDF converter—or why YAHTPC is not the best name for your service.

Throughout my career, I've found myself returning to the exact same architectural bottleneck over and over again. This week, I finally decided to engineer the definitive solution so I never have to build it again. I'm talking about backend HTML-to-PDF conversion. That's how I decided to build a service, which I call Slim Jim.

## The Problem

As a user, the expectation is straightforward: you want a perfect, 1-to-1 screenshot of your layout captured into a PDF file. But on the backend, the reality of rendering modern, rich frontends is incredibly heavy. For high-throughput, primitive documents like warehouse barcodes, thermal labels, and receipts, spinning up a headless browser (like Puppeteer or Chromium) inside a container is a massive resource drain.

I needed a lean, stateless compilation bridge. Here is how the architecture evolved:

## Iteration 1: The Zero-Dependency Dream

My first thought was to build a zero-dependency, manual parser. The plan was simple:

- Parse the incoming raw string, normalize the HTML, and handle the edge cases natively
- Take that clean structure and write PDF bytes manually while supporting standard HTML tags

Is it doable? Absolutely. It would have a microscopic memory footprint and be the perfect AWS Lambda serverless function. But engineering is about trade-offs. I realized this "romantic" MVP would quickly turn into a maintenance nightmare. A custom parser only survives as long as its original author actively supports it.

I traded the zero-dependency romance for long-term stability and pivoted.

## Iteration 2: The Pragmatic Architecture

I decided to leverage market-standard dependencies that specifically solved my core problems while easily clearing enterprise security audits.

**Problem 1: HTML Normalization.** Instead of writing a custom parser, I brought in BeautifulSoup. It perfectly handles messy string normalization and DOM structuring. When configured correctly, the execution overhead is minimal, and it is universally vetted by corporate security.

**Problem 2: Low-Level PDF Abstraction.** I wanted to interact with the PDF generation as closely as possible without writing raw bytes. I landed on ReportLab. The core engine is fully open-source, aggressively maintained, and acts as a bulletproof abstraction layer.

By wrapping these two tools in a clean Strategy pattern, I built the pipeline for Slim Jim.

## The Result

Currently, I've wrapped the engine with FastAPI and Mangum, making it an ultra-fast, drop-in serverless microservice ready for AWS Lambda deployments. However, the architecture is so decoupled that if you want to embed it directly into your own codebase as a standalone feature, you can drop the API layer entirely—BeautifulSoup and ReportLab are the only true dependencies you need.

Check it out, share your thoughts, drop a PR:
🔗 [Slim Jim Repository](https://github.com/NGUgeneral/slim-jim)
