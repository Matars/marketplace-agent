# marketplace-agent

Marketplace automation toolkit for finding second-hand deals and drafting sell listings.

The intended UX is simple: copy the prompt below into Hermes. Hermes handles cloning the repo, reading the repo guide/skills, installing the tool with `uv`, creating your workspace, configuring vendors/products, and running the first find workflow.

## Copy this into Hermes

```text
Set up marketplace-agent for me.

My goal:
I want to find GPUs that can run Qwen locally.

Default vendors:
Amazon and eBay.

Do this:
1. Clone or update https://github.com/Matars/marketplace-agent at ~/fafo/marketplace-agent.
2. Read ~/fafo/marketplace-agent/prompts/hermes-installation-guide.md first.
3. Follow that guide exactly.
4. Create or update my user workspace at ~/my-marketplace.
5. Do not configure demo vendors. Use real providers only: amazon and ebay by default.
6. If a provider plugin is missing or broken, use the repo vendor-builder skill and browser/browser-harness tools to implement or repair it.
7. Configure products/categories from my goal. For Qwen GPUs, prefer concrete GPU queries with enough VRAM.
8. Run the validation and find workflow from the guide.
9. Show me where the output JSON is and summarize what worked.

Safety:
- Do not auto-post sell listings.
- Do not message sellers or buyers.
- Do not bypass login/captcha/anti-bot protections without asking me first.
- Keep my personal workspace separate from the engine repo so future updates do not create git conflicts.
```

That is the user-facing setup. Everything else in this repo is for Hermes or contributors.

## What Hermes should read

The full installation/orchestration guide is here:

```text
prompts/hermes-installation-guide.md
```

Supporting repo skills:

```text
hermes/skills/marketplace-agent-workspace.md
hermes/skills/marketplace-agent-vendor-builder.md
hermes/skills/marketplace-agent-sell-draft.md
```

## Current status

Early prototype.

The project has the CLI/workspace foundation and Hermes prompt/skill workflow. Amazon and eBay are the desired default real providers, but their production provider plugins still need to be implemented and verified. Demo providers should not be part of the normal user workflow.
