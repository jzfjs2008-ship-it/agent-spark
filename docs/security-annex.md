# Security Annex

> **TODO:** This document is incomplete — original content was lost during a rename/migration.
> Contributions welcome to fill in the security architecture details for Agent Spark.

---

## interagent.json `security` field

```json
{
  "name": "code-reviewer",
  "version": "1.0.0",
  "api": { ... },
  "security": {
    "permissions": {
      "filesystem": {
        "read": ["src/**", "package.json", "*.md"],
        "write": []
      },
      "network": {
        "fetch": ["https://api.github.com/*"],
        "listen": []
      },
      "process": {
        "exec": ["node", "python3"],
        "env_read": ["PATH", "HOME"],
        "env_write": []
      },
      "context": {
        "read": ["current_file", "selection", "project_root"],
        "write": []
      }
    },
    "signing": {
      "algorithm": "ed25519",
      "signer": "did:key:z6MkhaXgBZDvB7rQmBKPkQ"
    },
    "sandbox": {
      "required": ["cpu_limit", "memory_limit", "network_filter"],
      "optional": ["fs_isolate"]
    }
  }
}
```

## Permission Model

| Category | Default | User-Overridable | Plugin-Declarable |
|----------|---------|-------------------|-------------------|

## Signing & Verification

```
       ▼
┌─────────────────────┐
│  interagent.json    │ ← signer (DID) + signature
└────────┬────────────┘
         ▼
┌─────────────────────┐
│  Bridge validates   │
└─────────────────────┘
```

## Trust Flow

```
1. Developer → InterAgent SDK → interagent.json
3. SDK validates signature against interagent.json
```

| Step | Actor | Action |
|------|-------|--------|

## Sandbox

```yaml
sandbox:
  filesystem:
    root: /tmp/interagent/{plugin_hash}/
  process:
```

| Resource | Default Limit | Configurable | Notes |
|----------|---------------|--------------|-------|

## Audit Trail

```
Audit log format: interagent.json (signed)
 ↓
 ↓
 ↓
 ↓
```

**Audit record:** `audit-{timestamp}.json`:

```json
{
  "plugin": {
    "name": "code-reviewer",
    "version": "1.0.0",
    "signer": "did:key:z6Mkha..."
  },
  "platform": "cursor",
  "declared_permissions": ["read:files"],
  "granted_permissions": ["read:files < src/**"],
  "denied_permissions": ["write:files (cursor unsupported)"],
  "bridge_version": "interagent-bridge-cursor@0.1.0",
  "timestamp": "2026-07-06T10:00:00Z"
}
```

---

## Cost Estimate

| Component | Effort | Risk | Notes |
|-----------|--------|------|-------|
| interagent.json Schema | Add `security.permissions` + `security.signing` | +3 | |

---

## Open Questions

```
(TODO: Fill in open security questions)
```
