# Gary 的散步旅行剪辑

Gary 个人的 Vlog 剪辑 skill。把每期明确确认的偏好保存为可版本管理、可继续调整的剪辑规范。

内容是剪辑指引、参考案例和校验工具；实际处理视频仍依赖使用环境中的 FFmpeg、剪辑软件及可访问素材。仓库不包含视频、照片、配乐文件或本机项目绝对路径。

## 剪辑风格

- 保留散步、旅行和露营的真实体验，尽量使用已有素材。
- 节奏紧凑，美照和纯过场默认停留1–2秒，重要对话按信息量保留。
- 关键转折交代清楚，字幕简短自然，不把事情说得更严重。
- 配乐克制，为现场讲话、雨声和脚步声留空间，不循环短声音凑时长。
- 按拍摄模式判断色彩还原，避免普通色彩误套 Log LUT、重复套 LUT。
- 延续已确认的删改；每次交付保留清晰的版本与可继续编辑的依据。

完整规则见 [SKILL.md](SKILL.md)。每期的明确要求优先；不会强制每条视频都采用同一时长、故事或配乐。

## 使用

在能读取本机素材的 Codex 会话里输入：

```text
使用 $gary-vlog-edit，按我的风格精剪这期旅行视频。

素材目录：给出完整路径
这次经历：简单说说去了哪里、发生了什么
必须保留：……
需要删除：……
目标时长：……（可省略）
```

继续修改已输出的视频：

```text
使用 $gary-vlog-edit，继续修改最新版本。
把两张照片各缩到1.5秒，保留已确认的字幕和现场声音。
```

本仓库所在目录就是已安装的 skill 目录，修改后不用另外同步副本。

## 安装到另一台电脑

安装 Git。在终端执行下面的命令即可克隆公开仓库：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/gary-zengjiali/gary-vlog-edit.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/gary-vlog-edit"
```

如果目标目录已存在，先检查里面的修改，不覆盖它。素材目录在每次任务中提供，本机专属路径可放在 `.local/`，该目录不进入 Git。

## 持续维护

告诉 Codex“把这条偏好保存到 gary-vlog-edit skill”，并说明它是长期偏好还是仅本期适用。典型流程是：

1. 修改 [SKILL.md](SKILL.md) 中真正影响剪辑判断的规则。
2. 只在需要例子时补充 [references/](references/)；将一次性要求留在项目中。
3. 运行下面的校验，检查 `git diff`。
4. 更新 [CHANGELOG.md](CHANGELOG.md)，必要时调整 [VERSION](VERSION)，提交并推送。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
git diff
git status --short
```

GitHub Actions 在推送与拉取请求时运行相同校验。校验确认结构、引用、可移植性和媒体文件排除；实际风格是否合适，需要结合下一期剪辑与反馈判断。

在另一台电脑更新前，先看 `git status`，处理自己的未提交修改后执行 `git pull --ff-only`。不要为了更新覆盖本地工作。

## 文件

| 文件 | 作用 |
| --- | --- |
| `SKILL.md` | 实际执行的剪辑规范 |
| `agents/openai.yaml` | 展示名称与默认调用提示 |
| `references/qiandao-baseline.md` | 偏好来源与本期制作选择，已去掉本机绝对路径 |
| `scripts/validate.py` | 本地与 CI 共用的校验 |
| `CHANGELOG.md` / `VERSION` | 维护记录与版本号 |
| `.local/` | 不上传的本机项目状态（可选） |

仓库公开。GitHub 保存剪辑 skill 的源码与历史，实际视频素材和个人项目路径继续留在本机，不随源码上传。
