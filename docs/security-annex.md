# InterAgent 互操作协议 — 安全架构附件 v1.0

> 本附件是对主方案的补充。安全不是后加模块，而是嵌入协议设计的第一性原则。

---

## S0. 安全设计总纲

**核心原则 ①：最小权限交叉（Least Privilege Intersection）**

InterAgent 的权限模型 = **各平台权限集的交集**，不是并集。

```
插件声明的权限：read:files, write:files, network:fetch
         ↓  InterAgent 桥接器
MCP 端：read:files, write:files, network:fetch       ✅ 能力匹配
Cursor 端：read:files                                  ✅ 自动降级到交集
GPT Action 端：无文件权限                               ✅ 自动降级
```

**规则：** 桥接器永远不得授予超出插件声明的权限，即使目标平台原生支持更高权限。

**核心原则 ②：默认拒绝（Deny by Default）**

- 未声明的权限 → 拒绝
- 未声明的资源 → 不可访问
- 未声明的网络端点 → 不可连接

**核心原则 ③：可审计（Auditable by Design）**

每个桥接器必须记录：
1. 加载了哪个插件（名称 + 版本 + 签名指纹）
2. 映射到哪些平台权限
3. 实际执行的权限清单（降级后的交集）
4. 插件调用的日志（可选，桥接层截获）

---

## S1. Permission Model / 权限模型

interagent.json 中新增 `security` 字段：

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

### 权限粒度映射表

| InterAgent 权限 | MCP 映射 | Cursor 映射 | GPT Action 映射 |
|----------------|----------|-------------|-----------------|
| `filesystem.read` | `resources`（URI 匹配） | `.cursor/rules` 中声明的 glob | ❌ 不支持 → 降级报错 |
| `filesystem.write` | `tools`（带文件写能力） | `executeCommand` 受限 | ❌ 不支持 |
| `network.fetch` | `tools`（HTTP 工具） | `runScript` 中限制网络 | `actions` OpenAPI |
| `process.exec` | `tools`（需明确声明） | ❌ Cursor 限制 | ❌ 不支持 |
| `context.read` | `prompts` | `@` 上下文引用 | `context` 参数 |
| `context.write` | ❌ MCP 限制 | `insertText` / `applyEdit` | ❌ 不支持 |

**安全关键行为（安全级别自动映射）：**

| 插件行为 | MCP | Cursor | GPTs | 安全级别 |
|----------|-----|--------|------|---------|
| 只读文件 | ✅ | ✅ | ❌ | L1 安全 |
| 写入文件 | ✅ | ⚠️ 受限 | ❌ | L2 需确认 |
| 执行外部命令 | ✅ (需声明) | ❌ | ❌ | L3 高危 |
| 网络请求 | ✅ | ⚠️ 受限 | ✅ | L2 需确认 |
| 读取用户上下文 | ✅ | ✅ | ✅ | L1 安全 |

---

## S2. 签名链（Signing Chain）

### 架构

```
[开发者 ED25519 私钥]
       │ 签名
       ▼
┌─────────────────────┐
│  interagent.json    │ ← 包含 signer（公钥 DID）+ signature
│  API 声明 + 权限     │
│  + 安全策略          │
└────────┬────────────┘
         │ 桥接器验证签名
         ▼
┌─────────────────────┐
│  桥接器验证通过后    │
│  生成平台特定配置    │
│  （旁注：每一层       │
│   生成的代码也签名）   │
└─────────────────────┘
```

### 签名验证流程

```
1. 用户加载插件 → InterAgent SDK 读取 interagent.json
2. SDK 从 signer 字段解析公钥（DID 或 HTTPS URL）
3. SDK 验证 signature 字段是否匹配 interagent.json 内容
4. 验证通过 → 进入权限交叉计算
5. 验证失败 → 拒绝加载，报告「签名无效/未知发布者」
6. （可选）首次加载时显示发布者 DID + 指纹确认
```

### 信任锚

| 阶段 | 信任机制 |
|------|----------|
| MVP（v0.1） | 首次加载显示指纹，用户手动确认 |
| v0.2 | 注册表托管公钥，自动查询 |
| v0.5 | Key Transparency / Sigstore 集成 |

---

## S3. 沙箱运行时要求（Sandbox Runtime Specification）

InterAgent 规范要求所有桥接器实现**运行时沙箱**：

```yaml
sandbox:
  cpu_quota: 100ms/100ms    # 每 100ms 最多跑 100ms CPU
  memory_limit: 256MB       # 内存上限
  network: deny_by_default   # 仅允许 security.permissions 中声明的端点
  filesystem:
    root: /tmp/interagent/{plugin_hash}/
    read_only: true          # 除非显式声明 write
  process:
    max_children: 3          # 最多 fork 3 个子进程
    timeout: 30s             # 单次调用超时
```

**不同宿主的能力差异：**

| 宿主 | 沙箱支持 | InterAgent 行为 |
|------|---------|----------------|
| Claude Desktop (MCP) | ⚠️ 无原生沙箱 | 桥接器注入 resource limit 包装器 |
| Cursor | ✅ 进程隔离 | 利用 Cursor 已有的安全边界 |
| Sandboxed runtime (Docker) | ✅ 完整隔离 | 首选部署方式 |
| 浏览器 (GPTs) | ✅ 浏览器沙箱 | 受限最多，自动降级 |

---

## S4. 桥接器安全规范（Bridge Security Requirements）

每个平台桥接器在生成平台特定配置时，必须执行以下安全变换：

```
输入：interagent.json（已验证签名）
 ↓
Step 1：权限交叉计算
  → 当前平台能力 ∩ 插件声明权限 = 实际授予权限
  → 例：插件声明 write:files 但 Cursor 不支持
  → 结果：write:files 被静默降级，不报错
 ↓
Step 2：权限脱敏
  → glob 路径限制（不允许 ** 裸通配）
  → 网络端点白名单验证（不允许裸 *）
  → 环境变量白名单（不允许裸 access）
 ↓
Step 3：生成平台配置
  → MCP：生成配置含 resources + tools 严格声明
  → Cursor：生成 rules 含 glob 约束
  → GPTs：生成 actions 含 encoded auth
 ↓
Step 4：输出加签（可选）
  → 对生成的平台特定配置附加桥接器签名
  → 允许用户确认「此配置由 InterAgent v0.1 桥接器生成」
```

**桥接器自我审计：** 每次运行输出一份 `audit-{timestamp}.json`：

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

## S5. 安全与主方案的集成更新

对主方案中产品范围的更新：

| 模块 | 新增安全内容 | 工时影响 |
|------|-------------|----------|
| interagent.json Schema | 新增 `security.permissions` 字段 + `security.signing` | +3 天 |
| Python SDK | 签名验证 + 权限交叉计算 + 降级逻辑 | +5 天 |
| MCP 桥接器 | 能力声明检查 + audit log 生成 | +3 天 |
| Cursor 桥接器 | glob 约束 + 权限脱敏 | +3 天 |

**总开发周期影响：** W1-W6 → W1-W7（+1 周，纯安全）

**安全 MVP 范围（不妥协的底线）：**
- ✅ interagent.json 签名验证（必须，否则任何人都能冒充插件）
- ✅ 权限交叉计算（必须，否则跨平台时权限膨胀）
- ✅ 审计日志输出（必须，否则事件不可追溯）
- ⏳ 运行时沙箱（v0.2 再补，因为依赖宿主能力）
- ⏳ 桥接器签名（v0.2）

---

## S6. 已知安全局限（如实标注）

```
⚠️ InterAgent v0.1 以下安全问题已知但未在 MVP 完全解决：

1. 运行时沙箱依赖宿主平台能力
   → Claude Desktop 无原生沙箱，MCP 桥接器无法强制隔离
   → 缓解：在文档中标注"Claude Desktop 端安全等级低于 Cursor 端"

2. 签名信任锚问题
   → MVP 阶段由用户首次加载时手动确认指纹
   → 缓解：这不是 InterAgent 独有的问题，npm/pip 也面临同样的困境

3. 桥接器自身安全性
   → 如果桥接器本身被篡改，它可能绕过所有安全检查
   → 缓解：桥接器也签名，但 bootstrap 问题（谁签桥接器？）需后续版本解决

4. 权限声明的可信度
   → 插件开发者可能声明过少权限、实际做更多事（malicious plugin）
   → 缓解：这是平台侧的责任（MCP/Cursor 应限制插件执行环境）
          InterAgent 只确保权限不会跨平台「膨胀」
```
