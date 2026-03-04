# MemOS Cloud Skill

MemOS Cloud Server API 技能插件。该技能允许 Agent 或开发者直接调用 MemOS 云平台 API，实现记忆的检索、添加、删除以及反馈功能。

## 环境要求 (Prerequisites)

- **Python**: 3.x 及以上版本
- **Python 依赖**: `requests` 模块

如果你的环境中还没有 `requests`，可通过以下命令进行安装：

```plaintext
pip3 install requests
```

## 安装与引入 (Installation)

该技能已上传至 GitHub 仓库。

### 方式一：使用命令安装（推荐）

推荐使用 `skills` 命令进行安装：

```bash
npx skills add https://github.com/MemTensor/MemOS-Cloud-Skill
```

### 方式二：本地克隆并手动复制安装

1. 将本仓库克隆到本地：
   ```bash
   git clone https://github.com/MemTensor/MemOS-Cloud-Skill.git
   ```
2. 手动将技能文件夹复制到你对应的 agent 技能库目录中进行引入即可。

## 配置环境变量 (Environment Variables)

**这是最重要的一步！在执行任何 API 操作前，你必须确保以下环境变量已经配置。**

### 必填环境变量

1. **MEMOS**\_API_KEY:

   - `MEMOS_API_KEY`: 在MemOS官网\[API控制台\](https://memos-dashboard.openmem.net/cn/apikeys/)上注册账号，然后在接口密钥页面新建api-key并复制粘贴在此处。
   - ![image](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/v9kqDejjkRkrMOVx/img/aa5b288a-ef60-454c-96cb-ad01c726c4e9.png)
2. **MEMOS**\_USER_ID:

   - **定义**：确定性的用户自定义个人标识符。
   - **安全提示**：请不要使用随机值、设备 ID 或聊天会话 ID 作为用户标识符。对于同一用户，该标识符需要在不同设备/客户端中保持一致。
   - **推荐使用**：个人 email 地址的哈希值、姓名全称或员工 ID。

---

### 如何在不同操作系统中配置环境变量？

#### Windows

**方式一：通过 PowerShell 临时生效 (当前窗口)**

```plaintext
$env:MEMOS_API_KEY="你的_API_KEY"
$env:MEMOS_USER_ID="你的_USER_ID"
```

**方式二：通过 CMD 临时生效 (当前窗口)**

```plaintext
set MEMOS_API_KEY=你的_API_KEY
set MEMOS_USER_ID=你的_USER_ID
```

**方式三：永久生效 (推荐)** 按 `Win + R` 键，输入 `sysdm.cpl` 后回车。进入“系统属性” -> “高级” -> “环境变量”。在你的“用户变量”中点击“新建”，分别添加名为 `MEMOS_API_KEY` 和 `MEMOS_USER_ID` 的变量与值。最后重启你的终端。

#### Linux / macOS

**临时生效 (当前终端窗口)**

```plaintext
export MEMOS_API_KEY="你的_API_KEY"
export MEMOS_USER_ID="你的_USER_ID"
```

**永久生效 (推荐)** 编辑你的 Shell 配置文件（如 `~/.bashrc` 或 `~/.zshrc`），在文件末尾添加以下内容：

```plaintext
export MEMOS_API_KEY="你的_API_KEY"
export MEMOS_USER_ID="你的_USER_ID"
```

保存后，在终端执行 `source ~/.bashrc` 或 `source ~/.zshrc` 使配置立刻生效。

---

## 功能与使用

安装并配置成功后，您的 AI 助手（如 Trae, Cursor 等）将自动获得以下记忆管理能力。您可以直接使用自然语言与助手交互。

### 核心功能

- **记录记忆**：保存重要的事实、偏好或对话内容。
- **检索记忆**：根据问题自动查找相关的历史信息。
- **遗忘记忆**：删除不再需要或错误的信息。

### 交互示例

**场景 1：添加记忆**

> "请记住我住在上海，平时喜欢在周末去跑步。" "记录一下，我的开发首选语言是 Python。" ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/vBPlN5jjQoaKROdG/img/56ebdd17-17d9-4bae-96e5-f936c4adb006.png)

**场景 2：查询记忆**

> "我之前说过我住在哪里吗？" "我有哪些饮食偏好？" ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/vBPlN5jjQoaKROdG/img/49cc3bcd-5e92-46bc-ac67-375b2270929e.png)

**场景 3：删除记忆**

> "删除关于我喜欢吃西红柿的记忆。" "忘记我之前的居住地址。" ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/vBPlN5jjQoaKROdG/img/5bf3a927-3a18-41fe-9b64-ce5166897dbc.png)
