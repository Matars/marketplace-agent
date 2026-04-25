# Hermes bootstrap prompt for marketplace-agent

Use this prompt when you want Hermes to install/configure marketplace-agent from a natural-language goal.

```text
You are configuring marketplace-agent for me.

Goal:
<describe what I want to find or sell>

Default workflow:
1. Install or update marketplace-agent from https://github.com/Matars/marketplace-agent using uv.
2. Create or update a separate user workspace, not the engine repo.
3. Load/use the repo skills:
   - marketplace-agent-workspace
   - marketplace-agent-vendor-builder
   - marketplace-agent-sell-draft
4. Convert my natural-language goal into concrete marketplace categories and product queries.
5. Configure marketplace.toml in the workspace.
6. If a requested vendor is missing, inspect the marketplace with browser/browser-harness tools and build a vendor plugin.
7. Run `marketplace-agent doctor <workspace>`.
8. Run `marketplace-agent find <workspace>` for find workflows.
9. Inspect `<workspace>/output/latest.json` and summarize results.
10. For sell workflows, create JSON listing drafts only. Do not auto-post listings or message buyers unless I explicitly approve the exact action.

Safety:
- Do not auto-post.
- Do not bypass captchas/login protections without asking.
- Keep user config outside the engine repo to avoid git conflicts.
```
