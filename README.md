# marketplace-agent

Marketplace automation toolkit for finding marketplace deals and drafting sell listings.

The intended UX is simple: copy the prompt below into Hermes. Hermes handles setup, asks you onboarding questions, creates your workspace, configures vendors/products, and runs the first workflow.

## Copy this into Hermes

```text
Set up marketplace-agent for me.

Do this:
1. Clone or update https://github.com/Matars/marketplace-agent with submodules enabled.
2. Read the repo file prompts/hermes-installation-guide.md first.
3. Follow that guide exactly.
4. Start onboarding by asking me the required setup questions from the guide.
5. After I answer, create or update a separate user workspace outside the engine repo.
6. Configure marketplace-agent from my answers.
7. Do not configure demo vendors unless I explicitly ask for a dry-run placeholder.
8. Use the bundled browser-harness submodule at third_party/browser-harness for vendor discovery/scraper repair.
9. If a provider plugin is missing or broken, use the repo vendor-builder and browser-harness skills to implement or repair it.
10. Run validation and the requested workflow from the guide.
11. Show me where the output JSON or draft JSON is and summarize what worked.

Safety:
- Do not auto-post sell listings.
- Do not message sellers or buyers.
- Do not bypass login/captcha/anti-bot protections without asking me first.
- Keep my personal workspace separate from the engine repo so future updates do not create git conflicts.
```

That is the user-facing setup. Everything else in this repo is for Hermes or contributors.

## What Hermes should read

The full onboarding/installation/orchestration guide is here:

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

The project has the CLI/workspace foundation and Hermes prompt/skill workflow. Real provider plugins still need to be implemented and verified. Demo providers should not be part of the normal user workflow.
