# marketplace-agent

Marketplace automation toolkit for finding marketplace deals and drafting sell listings.

The intended UX is simple: copy the prompt below into Hermes, fill in your own goal, and let Hermes handle setup. Hermes clones the repo, reads the repo guide/skills, installs/runs the tool with `uv`, creates your workspace, configures vendors/products, and runs the first workflow.

## Copy this into Hermes

```text
Set up marketplace-agent for me.

My goal:
<describe what you want to find or sell, in your own words>

Preferred vendors:
<list marketplaces you want to use, or write "choose sensible defaults for my country">

Do this:
1. Clone or update https://github.com/Matars/marketplace-agent with submodules enabled.
2. Read the repo file prompts/hermes-installation-guide.md first.
3. Follow that guide exactly.
4. Create or update a separate user workspace outside the engine repo.
5. Do not configure demo vendors. Use real providers only unless I explicitly ask for a dry-run placeholder.
6. Use the bundled browser-harness submodule at third_party/browser-harness for vendor discovery/scraper repair.
7. If a provider plugin is missing or broken, use the repo vendor-builder and browser-harness skills to implement or repair it.
8. Configure products/categories from my goal.
9. Run the validation and requested workflow from the guide.
10. Show me where the output JSON or draft JSON is and summarize what worked.

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
hermes/skills/marketplace-agent-browser-harness.md
hermes/skills/marketplace-agent-sell-draft.md
```

Browser-harness is included as a full upstream submodule:

```text
third_party/browser-harness/
```

## Current status

Early prototype.

The project has the CLI/workspace foundation and Hermes prompt/skill workflow. Real provider plugins such as Amazon/eBay still need to be implemented and verified. Demo providers should not be part of the normal user workflow.
