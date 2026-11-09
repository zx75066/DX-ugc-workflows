# DX-ugc-workflows

**面向 Codex 的电商 UGC 视频 Skill：一个入口，三种执行模式，六条内容路线。**

[下载最新完整包](https://github.com/zx75066/DX-ugc-workflows/releases/latest) · [完整示例](示例需求.md) · [环境配置与常见问题](docs/安装与环境.md) · [反馈问题](https://github.com/zx75066/DX-ugc-workflows/issues)

## 三种模式都包含在内

| 模式 | 你准备什么 | Skill 做什么 | Higgsfield 生成调用 |
|---|---|---|---|
| **零积分** `reference-only-prompt` | 已有模特图 + 产品图 | 产品分析、口播、文本分镜、视频提示词、参考图顺序、验收清单 | 不调用 |
| **少积分 / 低积分** `soul-only-prompt` | 产品图，允许生成一张模特图 | 一张 Soul 2.0 模特图 + 上述文本交付 | 只生成一张模特图 |
| **完整视频** `full-render` | 所选路线所需的图片、产品信息或网页 | 按路线生成图片和视频，质检，并在需要时拼接和加字幕 | 按实际阶段调用 |

**零积分和少积分模式不会生成视频成片。** “零积分”指不使用 Higgsfield 生成积分；Codex 本身的使用限制与费用由你的账号决定。少积分不代表固定价格，实际费用以你自己的生成服务预检为准。

零积分和少积分适用于 **真人测评、试穿、教程、开箱** 四条路线；纯产品展示和网站 / SaaS 演示使用完整模式。已有模特图和产品图时，少积分请求会转为零积分，避免重复生成人物。

## 六条内容路线

| 路线 | 适用内容 |
|---|---|
| 真人产品测评 `ugc-flow` | 人物出镜口播、展示和评价产品 |
| 纯产品展示 `ugc-product-flow` | 产品为画面主体，配画外音 |
| 网站 / SaaS 演示 `ugc-saas-flow` | 真实网页截图、讲解和合成 |
| 试穿与穿搭 `ugc-try-on-flow` | 上身版型、穿着效果与面料 |
| 分步骤教程 `ugc-tutorial-flow` | 按真实顺序演示使用方法 |
| 开箱与揭晓 `ugc-unboxing-flow` | 从密封包装到产品揭晓 |

## 让智能体自动安装与加载

**不想自己操作终端，可以直接复制下面整段，发给具有项目文件访问和命令执行能力的智能体，例如 Codex。** 先在智能体中打开你要制作视频的项目文件夹；这段指令会让它完成下载、安装和检查。

```text
请帮我把 DX-ugc-workflows 安装到当前项目，并完成本地验证和加载。
仓库：https://github.com/zx75066/DX-ugc-workflows

请直接执行安装，而不是只给我操作教程：
1. 确认当前项目根目录；如果尚未打开或指定项目，先问我安装到哪个文件夹。
2. 获取仓库最新正式 Release 的完整 ZIP 和 SHA256SUMS.txt，核对 ZIP 校验值后解压到临时目录。先阅读包内 README.md 和 install.sh。
3. 检查 Python 3.9+。macOS/Linux 在解压目录运行 bash verify-package.sh，再运行 bash install.sh "项目绝对路径"。
   Windows 使用可用的 Python 命令核对包内 SHA256SUMS.txt，完整复制 skill 目录到下面的目标位置；不要直接在 PowerShell 运行 Bash 脚本。
4. 最终安装位置必须是：
   <项目根目录>/.agents/skills/higgsfield-ugc-workflows/
   该目录下直接包含 SKILL.md、agents、references、scripts、workflows，以及六条子流程。保留 higgsfield-ugc-workflows 这个内部名称。
5. 如果已安装且内容相同，跳过重复复制；如果版本或内容不同，先备份旧目录到项目 .agents/skill-backups/ 下，再更新。macOS/Linux 可以使用安装器的 --replace；保留原有其他 Skills。
6. 从项目根目录运行以下检查（Windows 根据环境将 python3 替换为 python 或 py -3）：
   python3 .agents/skills/higgsfield-ugc-workflows/scripts/local_workflow_registry.py catalog
   python3 .agents/skills/higgsfield-ugc-workflows/scripts/check_mode_contracts.py
   必须确认列出六条工作流，且模式检查 valid 为 true、errors 为空。
7. 读取已安装的 SKILL.md，确认包含 reference-only-prompt、soul-only-prompt、full-render 三种模式。如果当前智能体支持原生 Skill 发现，尝试发现 $higgsfield-ugc-workflows；如果需要新一轮对话、重新打开项目或重启应用，请说明实际下一步。若当前智能体不支持这种 Skill 格式，请说明兼容性限制，不能把文件复制成功说成已原生加载。
8. 最后告诉我安装绝对路径、版本、验证结果、加载状态，以及三个模式各需要什么。缺少 Python 或其他条件时，说明具体阻碍及下一步。

本次任务只安装和检查 Skill。不开始制作内容，不上传素材，不调用付费生成，也不修改全局配置。MCP 尚未配置时说明即可，零积分模式不依赖 Higgsfield MCP。
```

安装完成后，在目标项目中开始新一轮对话，使用下方三个模式的示例。仓库名是 `DX-ugc-workflows`，实际调用名是 `$higgsfield-ugc-workflows`。其他智能体能否自动发现此 Skill，取决于其兼容性。

## 手动安装：下载、解压、安装到项目

1. 从 [Releases](https://github.com/zx75066/DX-ugc-workflows/releases/latest) 下载 `DX-ugc-workflows-v2.0.2.zip` 并解压。
2. 准备一个自己的项目文件夹，在终端进入解压后的 `DX-ugc-workflows-v2.0.2` 目录。
3. macOS / Linux 运行下列命令，将示例路径换成你的真实项目路径：

```bash
bash install.sh "/绝对路径/你的视频项目"
```

Windows 或手动安装：将包中的整个 `skill` 文件夹复制到项目里的 `.agents/skills/`，并命名为 `higgsfield-ugc-workflows`。最终必须能看到：

```text
你的视频项目/
└── .agents/skills/higgsfield-ugc-workflows/
    ├── SKILL.md
    ├── agents/
    ├── references/
    ├── scripts/
    └── workflows/  # 包含六条子流程
```

4. 在 Codex 中打开这个项目，开始新一轮对话。如果 Skill 未出现，重新打开项目或重启 Codex。

仓库名是 **DX-ugc-workflows**；为了保留已有工作流中的路径引用，调用名仍为 **`$higgsfield-ugc-workflows`**。本包采用项目本地安装，工作时从该项目根目录开始。

会使用 Git 的用户也可以：

```bash
git clone https://github.com/zx75066/DX-ugc-workflows.git
cd DX-ugc-workflows
bash install.sh "/绝对路径/你的视频项目"
```

## 三个可以直接复制的入口

将图片路径换成你本机可访问的真实文件。产品内容物的颜色、真实用法和卖点证据不足时，Skill 会先向你确认。

### 入口一：零积分

```text
使用 $higgsfield-ugc-workflows。
执行模式：零积分（reference-only-prompt）。
做一条 15 秒、9:16、英语的真人产品测评视频方案。
模特图：/你的项目/assets/model.png
产品图：/你的项目/assets/product.png
参考顺序：产品图第一，模特图第二。
请检查素材，输出口播、精确时间文本分镜、完整视频提示词、参考图顺序和验收清单。
不要调用远程生成服务。
```

### 入口二：少积分

```text
使用 $higgsfield-ugc-workflows。
执行模式：低积分（soul-only-prompt），只允许生成一张 Soul 2.0 模特图。
做一条 15 秒、9:16、英语的真人产品测评视频方案。
产品图：/你的项目/assets/product.png
模特：女性，28 岁左右，居家自然光。
先检查 MCP、素材和人物图费用；费用无法预检时先说明，生成前让我确认。
人物图中不要出现产品。生成后下载到本地，再输出口播、文本分镜和视频提示词。
```

### 入口三：完整视频

```text
使用 $higgsfield-ugc-workflows。
执行模式：完整渲染（full-render）。
制作一条 15 秒、9:16、英语的真人产品测评视频。
产品图：/你的项目/assets/product.png
模特：女性，28 岁左右，居家自然光。
请先检查可用工具、必要素材、预计生成阶段和费用，付费生成前让我确认。
通过检查后执行所需生成、质检，并返回成片。
```

## 环境要求

- **所有模式：** 支持项目 Skill 的 Codex 环境，以及 Python 3.9+。本地目录和模式检查只使用 Python 标准库。
- **零积分：** 已有本地人物图和产品图，不需要 Higgsfield MCP。
- **少积分：** 自行连接兼容的 Higgsfield MCP，具备 Soul 2.0 图片生成、任务查询和下载能力，并有可用额度。
- **完整视频：** 自行连接覆盖人物、分镜、图片精修、视频生成与任务查询等所需阶段的工具。网页、拼接、转写或字幕环节可能还需 Node.js、Playwright、FFmpeg / FFprobe、转写模型和字体。

**下载 Skill 不会自动安装 Higgsfield MCP，也不会提供账号、密钥或积分。** 本仓库未附带经过验证、可直接导入的 MCP 连接配置；远程模型和工具是否可用取决于你自己的服务。详见 [环境与常见问题](docs/安装与环境.md)。

## 验证与更新

在解压后的包或仓库根目录运行本地检查：

```bash
bash verify-package.sh
```

它会检查文件校验值、六条路线和提示词模式约束，不会调用付费生成服务。已经安装到项目的用户可运行：

```bash
python3 .agents/skills/higgsfield-ugc-workflows/scripts/local_workflow_registry.py catalog
python3 .agents/skills/higgsfield-ugc-workflows/scripts/check_mode_contracts.py
```

更新时下载新版本，在新版本目录执行 `bash install.sh "/你的项目路径" --replace`。旧版本会移到项目 `.agents/skill-backups/` 下的时间戳备份目录。

## 当前验证范围与来源

本次发行验证本地包完整性、六条路线读取和项目安装；未在粉丝账号或不同 MCP 服务上运行付费视频生成。完整流程为工作流指令，实际执行以实时工具接口和账号能力为准。

本项目为非官方工作流整理，来源与第三方内容说明见 [NOTICE.md](NOTICE.md)。请在反馈时提供操作系统、执行模式、失败步骤和去除密钥后的报错信息。
