---
title: Halepa – Lightweight AWS Alert Router
date: 2026-06-15
excerpt: A 15KB serverless alert bridge that routes AWS CloudWatch events to Discord, Telegram, and WhatsApp with zero cost and zero dependencies.
---

# Halepa – Lightweight AWS Alert Router

<img src="/assets/Halepa%20Image.jpg" alt="Halepa Alert Routing" class="vertical">

Instead of dealing with bloated libraries or third-party platforms to route my cloud alerts, I just wrote a 15KB script. It was the right call.

## The Trigger

We've all been there: You're wrapping up a product ecosystem deployment, focus shifts elsewhere, and you stop keeping a microscopic eye on the dashboard.

Long story short—one of my background services was silently struggling to recover from an edge-case exception for three days before I caught it.

My immediate reaction? "Time to get some real-time telemetry out of this cloud."

## The Challenge

Since this stack runs on AWS, I looked at the out-of-the-box defaults. Standard CloudWatch alerts wanted to push to email or SMS. No thanks—it's 2026, and our team lives inside Discord. I needed these infrastructure failures routed straight to a dedicated #alerts channel.

When I looked at existing market options to bridge the gap, I found two extremes:

1. **Massive, dependency-heavy open-source libraries** that require their own wrapping infrastructure anyway
2. **Third-party SaaS alert managers** that require routing our raw cloud telemetry out of our secure AWS environment to sit on someone else's platform

## The Solution: Halepa

I sketched out a minimal design pattern on a napkin: A completely stateless, zero-dependency event router.

A few hours later, the pipeline was live. The result is **Halepa**.

### Key Features

- **Tiny Footprint**: Built strictly within the Python standard library. The entire deployment package is a tiny 15KB zip archive
- **Minimal Overhead**: Because there is no dependency bloat to parse, it mounts directly to AWS Lambda memory with near-zero cold start overhead
- **Polymorphic Routing**: Intercepts native AWS SNS messages, normalizes the event payload, and handles routing across multiple channels simultaneously
- **Multi-Channel Support**: Seamlessly fans out alarms straight to Discord (as seen in screenshots), Telegram, and WhatsApp—all without ever touching a data store
- **Free Tier**: Runs completely on the AWS Lambda free tier. Operating cost: **$0.00**. Maintenance overhead: **Zero**

## Philosophy

Bloatware isn't something to be proud of. Building lightweight, deterministic, and highly focused software is.

I've just opened up the repository for Halepa. The core engine is fully functional, and I'm looking to expand the provider footprint even further next (Matrix protocol is up next on my radar).

If your team is looking for a lightweight, zero-cost alert bridge, give it a look, spin it up in your own sandbox, or drop a PR to add support for your team's favorite communication channels.

🔗 [Halepa Repository](https://github.com/NGUgeneral/halepa)
