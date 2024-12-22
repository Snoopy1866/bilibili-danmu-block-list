# bilibili-danmu-block-list

本仓库收集哔哩哔哩弹幕屏蔽规则，。

## 如何使用

1. 前往 [Release](https://github.com/Snoopy1866/bilibili-danmu-block-list/releases) 下载最新版规则文件。

2. 进入任意哔哩哔哩视频页面，点击 `弹幕列表` 右侧的 ⠇，选择 `屏蔽设定`：
   ![step1](res/how-to-use-step-1.png)

3. 在内容空白处右键，选择 `导入json文件`：
   ![step2](res/how-to-use-step-2.png)

4. 在弹出的窗口中，找到在步骤 1 中下载的 json 文件，点击 `打开` 即可。

## `bilibili-danmu-blocklist.json` 字段解释

### 哔哩哔哩的字段：

| 名称     | 含义           | 类型      | 必要性     | 取值                                                                        |
| -------- | -------------- | --------- | ---------- | --------------------------------------------------------------------------- |
| _type_   | 规则类型       | _int_     | _required_ | <ul><li>0（屏蔽文本）</li><li>1（屏蔽正则）</li><li>2（屏蔽用户）</li></ul> |
| _filter_ | 规则内容       | _string_  | _required_ | _Any_                                                                       |
| _opened_ | 规则是否启用   | _boolean_ | _required_ | <ul><li>true</li><li>false</li></ul>                                        |
| _id_     | 规则唯一标识符 | _int_     | _optional_ | _Any_                                                                       |

> [!NOTE]
>
> - `id` 字段暂未启用

### 本仓库添加的字段：

| 名称              | 含义         | 类型           | 必要性     | 可选值 |
| ----------------- | ------------ | -------------- | ---------- | ------ |
| _description_     | 规则描述     | _string_       | _optional_ | _Any_  |
| _examples_        | 规则匹配示例 | _list[string]_ | _optional_ | _Any_  |
| _excludeExamples_ | 规则排除示例 | _list[string]_ | _optional_ | _Any_  |

> [!NOTE]
>
> `excludeExamples` 字段用于辅助正则表达式的编写，尽可能避免错杀正常弹幕。

## 如何清空现有规则

分别切换到 `屏蔽文本`、`屏蔽正则` 标签，按 `F12` 打开开发者工具，在 `控制台` 中执行以下代码：

```javascript
document
  .querySelectorAll("span.bpx-player-block-list-delete")
  .forEach((button) => {
    button.click();
  });
```

## 如何贡献

推荐使用 [VSCode](https://code.visualstudio.com/Download) 编辑规则文件。

前置要求

- [Python](https://www.python.org/downloads) >= 3.12
- [Git](https://git-scm.com/downloads) >= 2.45
- [uv](https://docs.astral.sh/uv/getting-started/installation) >= 0.5.9

1. 克隆本仓库

   ```bash
   git clone https://github.com/Snoopy1866/bilibili-danmu-block-list.git
   ```

2. 初始化项目

   ```bash
   uv sync
   ```

3. 新建一个分支，名称任意（例如：`feat`）

   ```bash
   git checkout -b feat
   ```

4. 修改 `bilibili-danmu-blocklist.json`

5. 提交更改并推送

   ```bash
   git add .
   git commit -m "feat: new rules"
   git push origin feat
   ```

6. 发起 Pull Request

> [!IMPORTANT]
>
> 1. 请不要添加 `type=2` 的规则，这类规则用于屏蔽指定 UID 的用户发出的弹幕，你应该自行添加这类规则，而不是在公共仓库中添加。
> 2. 修改或添加 `屏蔽正则` 规则时，需使用 `\\` 代替 `\`，例如：使用 `\\d+` 代替 `\d+`，这是因为 json 字符串本身需要对字符 `\` 进行转义。

## 相关链接

- [正则表达式指南](https://docs.python.org/zh-cn/3.13/howto/regex.html)
- [正则表达式可视化](https://jex.im/regulex)
- [正则表达式测试](https://www.jyshare.com/front-end/854)

## 类似的仓库

- https://github.com/jnxyp/Bilibili-Block-List
- https://github.com/zornlemma/bilibili_RE_block_list
- https://github.com/fang2hou/Bilibili-block-list
