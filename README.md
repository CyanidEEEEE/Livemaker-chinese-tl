# LiveMaker 游戏汉化详细教程

本教程详细介绍了 LiveMaker 引擎游戏的汉化方法，并着重解决了现有教程中存在的一些问题（例如无法加密、编码问题等）。本教程基于作者汉化《黑礁》2、3 的经验总结而成。

**注意：** 本教程仅供学习和研究使用，请勿用于任何商业用途或非法活动。对于因使用本教程而产生的任何问题或后果，作者概不负责。


---

## 工具准备

1.  **Pylivemaker:**
    *   **作用：** 用于解包、封包、转换 LiveMaker 游戏资源。
    *   **来源：** [GitHub](https://github.com/pmrowla/pylivemaker)
    *   **安装：**
        ```cmd
        pip install pylivemaker
        ```
     *  根据pylivemaker作者要求Python>=3.8，可通过Conda安装，或[官网](https://www.python.org/downloads/) 下载最新版本

2.  **FontCreator:**
    *   **作用：** 用于编辑字体文件，替换字符。
    *   **类型：** 商业软件（付费软件）

3.  **OpenOffice 或 LibreOffice:**
    *   **作用：** 用于编辑 CSV 格式的剧本文件。
    *   **来源：** [LibreOffice 官网](https://www.libreoffice.org/)

4.  **Locale.Emulator:**
    *   **作用：** 用于模拟特定区域设置（Locale）运行程序，解决乱码问题。
    *   **来源：** [GitHub](https://github.com/xupefei/Locale-Emulator)

5.  **GraphicsGale:**
    *   **作用：** 用于转换 LiveMaker 特殊的图片格式。
    *   **来源：** [GraphicsGale 官网](https://graphicsgale.com/us/download.html)

---

## 汉化流程

### 1. 解包游戏资源

1.  **打开命令行：** 在游戏 `.exe` 文件所在的目录下，打开命令行窗口（CMD）。
2.  **解包：** 使用 Pylivemaker 的 `lmar` 命令解包游戏资源：
    ```cmd
    lmar x game.exe -o game_files
    ```
    *   `game.exe`：替换为您的游戏 `.exe` 文件名。
    *   `game_files`：您可以自定义解包后的文件夹名称。

### 2. 提取并翻译剧本

1.  **寻找剧本文件：** 在解包后的文件夹中，找到最大的 `.lsb` 文件，这通常就是剧本文件（例如 `00000033.lsb`）。
2.  **转换为 CSV：** 使用 Pylivemaker 的 `lmlsb` 命令将 `.lsb` 文件转换为 CSV 文件：
    ```cmd
    lmlsb extractcsv --encoding=utf-8-sig 00000033.lsb 00000033.csv
    ```
    *   `--encoding=utf-8-sig`：指定编码为 UTF-8 with BOM，避免中文乱码。
3.  **编辑 CSV：** 使用 OpenOffice 或 LibreOffice 打开生成的 CSV 文件。
    *   **打开参数：**
        *   字符集：`Unicode (UTF-8)`
        *   分隔符：`逗号`
        *   文本分隔符: `"`
    *   **翻译：** 将 "Translated text" 列中的文本翻译为中文。
        *   **注意换行符：** 保持原文的换行符格式。在单元格中按下 `Ctrl + Enter` 可以输入换行符。

### 3. 处理编码问题（CP932）

**问题：** LiveMaker 引擎仅支持 CP932 编码，直接导入翻译后的文本会导致错误。

**解决方案：** 替换字体文件。

1.  **原理：** LiveMaker 通常默认使用 MS Gothic 字体。我们可以修改 MS Gothic 字体，将 CP932 中不常用的字符替换为汉字。
2.  **CP932 字符集：** [参考链接](https://uic.win/zh-hant/charset/show/cp932/)
3.  **修改字体（可选）：**
    *   我提供了一份修改过的 LiveMaker 字体（基于思源黑体）和替换表。
    *   如果您需要添加新的字符，可以使用 FontCreator 进行替换。
4.  **简繁转换：** 在使用我提供的替换表之前，建议先将文本进行简繁转换（简体转繁体），因为我已将简繁体不同的字体合并，统一显示为简体字形。CP932 中的繁体字多于简体字，因此使用繁体文本可以减少需要导入的新字符数量。
5.  **导回翻译文本:** 使用 Pylivemaker 的 `lmlsb` 命令将翻译后的 CSV 文件导回到 `.lsb` 文件：
    ```cmd
    lmlsb insertcsv --encoding=utf-8-sig 00000033.lsb 00000033.csv
    ```

### 4. 修改 UI 图片（可选）

1.  **使用 GraphicsGale：** LiveMaker 的图片格式特殊，需要使用 GraphicsGale 进行转换。
2.  **处理 Alpha 通道：**
    *   GraphicsGale 转换出的 PNG 图片带有 Alpha 通道，可能难以编辑。
    *   **分离 Alpha 通道：** 使用 `Image` -> `Duplicate Alpha Channel` 将 Alpha 通道分离。
    *   **导出编辑：** 将图片导出为其他格式进行编辑，或者在 GraphicsGale 中直接编辑。
    *   **恢复 Alpha 通道：** 编辑完成后，使用 `Image` -> `Make Alpha Channel`，选择 `Luminance` 并选择之前分离的 Alpha 通道图片，即可恢复 Alpha 通道。

### 5. 修改选项文本（可选）

1.  **导出 XML：** 选项文本通常不在 CSV 文件中。使用以下命令将 `.lsb` 文件转换为 XML 格式：
    ```cmd
    lmlsb dump --encoding=utf-8 00000033.lsb --mode xml --output-file 00000033.xml
    ```
2.  **查找文本：** 在 XML 文件中找到选项文本所在的位置，记录下对应的 `LineNo` 值。
3.  **编辑文本：** 使用以下命令编辑指定行的文本：
    ```cmd
    lmlsb edit 00000033.lsb XXX
    ```
    *   `XXX`：替换为文本所在的 `LineNo` 值。
    *   **注意：** 除了文本内容，尽量不要修改其他内容。

### 6. 修改其他参数（可选）

1.  **查找参数文件：** 根据您的需要，查找包含需要修改的参数的文件（例如，在我的汉化项目中，字体显示参数位于 `メッセージボックス作成.lsb`）。
2.  **导出 XML：** 使用 `lmlsb dump` 命令将文件转换为 XML 格式：
    ```cmd
    lmlsb dump --encoding=utf-8 メッセージボックス作成.lsb --mode xml --output-file メッセージボックス作成.xml
    ```
3.  **修改参数：** 参考第五步的方法，修改 XML 文件中的参数。

### 7. 发布汉化补丁

**建议：** 不要直接发布完整的游戏文件，而是利用 LiveMaker 优先调用外部文件的特性，发布补丁。

1.  **整理文件：** 将需要修改的文件（例如 `.lsb`、字体文件、修改后的图片等）整理到一个文件夹中。
2.  **发布补丁：** 让用户将原版游戏 `.exe` 文件放在补丁文件夹中，即可使用汉化补丁。

---
