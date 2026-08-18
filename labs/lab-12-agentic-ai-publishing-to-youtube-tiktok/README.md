# Lab 12 — Agentic AI Publishing to YouTube & TikTok

**Topic 03:** Apply New AI Technologies to Improve Video Production  
**Maps to:** A7 — adopt agentic AI to close the pipeline from edit to publish  
**Tools:** VEED export, ChatGPT/Claude (agent), YouTube Studio, TikTok, n8n/Zapier (optional)

## Goal

Close the GenAI video pipeline with an agentic step: export platform-ready cuts, then let an AI agent draft the title, description, hashtags and thumbnail concept, and push the video to YouTube and TikTok — scheduling included — while you stay in review control.

## What you'll build

Your video live (unlisted) on YouTube and/or TikTok, published via an agent-assisted workflow with AI-drafted metadata.

## Prompts

**Publishing kit**

```prompt
You are my publishing agent. For this 45-second video promoting an online learning platform, produce: 3 SEO YouTube title options under 60 characters, a 2-paragraph description with a call-to-action and link placeholder, 10 YouTube tags, a TikTok caption under 150 characters with 5 hashtags, a thumbnail concept (composition, text overlay, colours), and the best posting time for the Singapore audience. Present it as a checklist I can approve item by item.
```

**Agentic automation spec**

```prompt
Design an n8n workflow that: watches a Google Drive folder for a new MP4, drafts YouTube metadata with an LLM node, waits for my approval via email, then uploads to YouTube with the approved metadata and posts the link to Slack. List the nodes and the data passed between them.
```

## Step-by-step

1. Export two cuts from VEED: 16:9 1080p for YouTube and 9:16 for TikTok/Shorts, captions burned in for the vertical cut.
2. Ask an AI agent to draft the publishing kit: SEO title options, description with timestamps and links, 10 hashtags per platform, and a thumbnail concept.
3. Generate the thumbnail with the AI image generator from the agent's concept, and review the full kit — you approve every word before it ships.
4. Publish to YouTube: upload the 16:9 cut in YouTube Studio (set to Unlisted for class), paste the agent's title/description/tags, upload the thumbnail, and schedule the release time the agent recommends.
5. Publish to TikTok: upload the 9:16 cut, apply the agent's caption and hashtags, and schedule at the recommended engagement window.
6. Optional — automate: wire an n8n/Zapier flow (or a computer-use agent) that watches a Drive folder and performs the upload + metadata steps automatically, keeping a human-approval gate before anything goes live.
7. Verify both posts, then reflect: which pipeline stages (script → video → audio → edit → publish) are now AI-assisted, and where must a human stay in the loop?

## Check your work

The video is live (unlisted) on at least one platform with agent-drafted, human-approved metadata, and you can describe where the approval gate sits in the agentic flow.

---
*Tertiary Infotech Academy Pte Ltd · TGS-2024043855 · v7*
