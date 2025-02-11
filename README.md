# LiveMaker 游戏汉化教程

**本教程主要针对 LiveMaker 引擎游戏的剧情文本汉化。** 图片和选项的修改不在本教程范围内。

**注意：** 本教程仅供学习和研究使用，请勿用于任何商业用途或非法活动。对于因使用本教程而产生的任何问题或后果，作者概不负责。

**所需基础：**

*   Python 基础
*   正则表达式基础
*   JSON 语法
*   CSV 基础

---

## 工具准备

1.  **Pylivemaker:**
    *   **作用：** 用于解包和封包 LiveMaker 引擎的游戏资源。
    *   **来源：** [GitHub](https://github.com/pmrowla/pylivemaker)
    *   **安装：**
        ```cmd
        pip install pylivemaker
        ```
        *  根据pylivemaker作者要求Python>=3.8，可通过Conda安装，或[官网](https://www.python.org/downloads/) 下载最新版本
    *   **用法示例：**
        ```cmd
        cd /d "D:\livemaker游戏exe所在的路径"<br>
        lmar x game.exe -o 解包文件夹名
        ```

2.  **FontCreator:**
    *   **作用：** 用于编辑字体文件，替换字符。
    *   **类型：** 商业软件（付费软件）

3.  **Locale.Emulator:**
    *   **作用：** 用于模拟特定区域设置（Locale）来运行程序，解决乱码问题。
    *   **来源：** [GitHub](https://github.com/xupefei/Locale-Emulator)
    *   **安装:** 点Release发行版下载

4.  **SExtract:**
    *   **作用：** 用于从 CSV 文件中提取文本，并生成 JSON 文件，方便翻译工具处理。
    *   **来源：** [GitHub](https://github.com/satan53x/SExtractor)
    *   **安装：**
        ```cmd
        git clone git@github.com:satan53x/SExtractor.git
        cd SExtractor
        安装依赖.bat  
        运行.bat     
        ```
    *   **注意:** SExtract要求Python>=3.9版本

5.  **AI 翻译工具 (AiNiee 或 GalTransl):**
    *   **作用：** 用于对提取的文本进行机器翻译。
    *   **来源：**
        *   AiNiee: [GitHub](https://github.com/NEKOparapa/AiNiee)
        *   GalTransl: [GitHub](https://github.com/cx2333-gt/GalTransl)

6.  **UniversalInjectorFramework:**
    *   **作用:** 用于修改游戏字体
    *   **来源：** [GitHub](https://github.com/AtomCrafty/UniversalInjectorFramework)

---

## 汉化流程

### 1. 解包游戏资源

1.  **打开命令行：** 使用 Win+R 或 Win+Q 搜索 "cmd"，打开命令提示符。
2.  **切换目录：** 使用 `cd` 命令切换到游戏所在的目录：
    ```cmd
    cd /d "D:\livemaker游戏exe所在的路径"
    ```
3.  **解包：** 使用 Pylivemaker 的 `lmar` 命令解包游戏资源：
    ```cmd
    lmar x game.exe -o 解包文件夹名（随意命名）
    ```

### 2. 提取剧本文本

1.  **寻找剧本文件：** 在解包出来的文件夹中，找到最大的 `.lsb` 文件，通常这就是剧本文件（例如 `00000033.lsb`）。
2.  **转换为 CSV：** 使用 Pylivemaker 的 `lmlsb` 命令将 `.lsb` 文件转换为 CSV 文件：
    ```cmd
    lmlsb extractcsv --encoding=utf-8-sig 00000033.lsb 00000033.csv
    ```
    *   `--encoding=utf-8-sig`：指定编码为 UTF-8 with BOM，避免中文乱码。

### 3. 提取 CSV 文本并转换为 JSON

1.  **使用 SExtract：** 打开 SExtract 工具。
2.  **配置 SExtract：**
    *   引擎：选择 "JSON"
    *   规则：选择 "CSV"
    *   修改配置：
        ```
        22_search=^([\s\S]+)
        extraData=^Original text$
        writeOffset=1
        ```
    *   `writeOffset=1`：表示将翻译后的文本写入到 "Original text" 列右侧的 "Translated text" 列。
    *   您可以根据需要修改正则表达式 (`regex`) 来过滤和提取文本。
3.  **提取文本：** 点击 SExtract 的提取按钮，生成 `ctrl` 和 `new` 文件夹。
    *   `ctrl` 文件夹包含提取的文本的 JSON 文件。
4.  **使用AiNiee翻译:** 如果使用AiNiee工具选择该文件进行翻译，保存读取都选同一个ctrl路径，翻完了AiNiee新建`transDic.output_transDic.json.json`文件，将把文件修改至`transDic.json`覆盖原文件(注意备份)。

### 4. 翻译文本

1.  **选择翻译工具：** 使用 AiNiee 或 GalTransl 等 AI 翻译工具进行翻译。
2.  **翻译设置：** 参考您选择的 AI 翻译工具的文档，进行相应的设置。
3.  **翻译建议：** 建议使用云端大模型进行翻译，因为本地模型速度较慢。
    *   如果您有高性能显卡（显存 20G-50G），可以考虑使用 CausalLM-35B 或 Sakura 部署本地大模型。
4.  **JIS 注入：** 在 SExtract 设置中勾选 "JIS 注入"，确保生成的 JSON 文件中的文本都是日文（CP932 字符），避免后续导入时报错。

### 5. 导回翻译文本

1. **注入文本：** 在 SExtract 中点击 "注入" 按钮，它会在 `new` 文件夹下生成新的 CSV 文件。
2. **替换 CSV 文件** 把这个 CSV 文件放回原来的`解包文件夹名`目录覆盖原 CSV 文件（注意备份）
3.  **使用lmlsb导回:** 使用 Pylivemaker 的 `lmlsb` 命令将翻译后的 CSV 文件导回到 `.lsb` 文件：
    ```cmd
    lmlsb insertcsv --encoding=utf-8-sig 00000033.lsb 00000033.csv
    ```

**注意：**

*   如果未勾选 "生成 UniversalInjector 的 JIS 替换配置"，直接将翻译文本的 CSV 转换为 LSB 文件，可能会报错，提示存在大量不属于 CP932 的字符。
*   Pylivemaker 的 `lmlsb` 命令只支持 JIS 编码导入（LiveMaker 引擎仅支持 CP932 代码页）。
*   **解决方法：**
    *   在 SExtract 设置中勾选 "生成 UniversalInjector 的 JIS 替换配置"，将 CSV 文件中的 GBK 编码字符转换为 JIS 字符。

### 6. 封包并替换字体

1.  **封包：** 将修改后的 `.lsb` 文件与游戏主程序（`.exe`）放在同一个目录下。使用 `lmpatch` 命令进行封包。
    ```cmd
    lmpatch some.exe 00000001.lsb 
    ```
    *   这将生成一个新的 `.exe` 文件。
2.  **测试:** 使用 Locale.Emulator 打开游戏，如果发现日文字符修改成功了，只需要做下面任意字体方案即可，其中方案3.（2） 最快捷

3.  **字体解决方案：**
    *   **方案 1：使用 UniversalInjectorFramework (UIF):**
        *   **原理：** 通过伪装系统 DLL，让游戏优先加载 UIF 的 DLL，从而实现字体替换。
        *   **参考链接：** [GitHub](https://github.com/AtomCrafty/UniversalInjectorFramework)
        *   **预编译 DLL：** [GitHub](https://github.com/satan53x/SExtractor/tree/552ce5dc254c6623d5b21b928486c48d90fa32fd/tools/UniversalInjectorFramework)
        *   **步骤：**
            1.  选择一个 DLL（例如 `winmm.dll`）。
            2.  SExtract 在设置中勾选 "生成 UniversalInjector 的 JIS 替换配置" 后，`ctrl` 文件夹会生成 `uif_config.json` 文件。
            3.  将 `uif_config.json` 和选择的 DLL 复制到游戏根目录。
            4.  打开 `uif_config.json`，启用相关配置。
            5.  （可选）将 `uif_config.json` 中的 `allocate_console` 设置为 `true`，启用控制台输出，查看 DLL 是否加载成功以及是否捕获到字体函数。
    *   **方案 2：UIF 启用字体更换:**
        *    配置文件通过启用font_manager自行加载
    *   **方案 3：替换字体文件：**
        1.  **原理：** LiveMaker 通常默认调用 MS Gothic 字体。我们可以修改 MS Gothic 字体，将 CP932 中不常用的字符替换为我们需要的字符。
        2.  **CP932 字符集：** [Win கீழ்](https://uic.win/zh-hant/charset/show/cp932/)
        3.  **修改过的字体和替换表（可选）：** 我提供了一份修改过的 LiveMaker 字体（基于思源黑体）和替换表。如果您需要添加新的字符，可以使用 FontCreator 进行替换。
        4.  **简繁转换：** 在使用我提供的替换表之前，建议先将文本进行简繁转换（简体转繁体），因为我已将简繁体不同的字体合并，统一显示为简体字形。CP932 中的繁体字多于简体字，因此使用繁体文本可以减少需要导入的新字符数量。
        5.  **otfcc批量更换（可选）:** 如果不想使用FontCreator手动更换字体，可以使用otfcc提供的工具批量更换字体，详细参见本仓库目录的`JIS字体批量替换`的脚本`font_CN_JP.py`
        6.  **安装字体:** 安装[字体](https://github.com/satan53x/SExtractor/tree/552ce5dc254c6623d5b21b928486c48d90fa32fd/tools/Font) 提供的ttf文件，只要是SE转换的JIS字体，转区启动游戏均为能显示中文字体

    *   **疑难解答：**
        *   如果安装字体后仍然无法显示中文：
            1.  重启电脑。
            2.  在`解包文件夹名`导出文件夹中，[cmd批量执行](https://github.com/allrobot/Translator-_and_others_script/tree/main/%E8%84%9A%E6%9C%AC/livemaker%E5%BC%95%E6%93%8E) `lmlsb dump xxx.lsb > xxx.lsb.txt`，打开notepad++启用文件查找`font`看看是lm引擎用的哪个字体文件.
            3.  部分字体没有显示为中文，打开FontCreator搜目标JIS字体，把另一个黑体文件中的简体字复制黏贴到搜到的JIS字体，或使用`font_CN_JP.py`要求的`subs_cn_jp.json`字典添加{"要求显示的中文x":"游戏显示的日文x"}，导出为ttf然后安装重启PC。
            4.  系统的MSPGothic并没有被SExtract提供的字体文件覆盖掉(即使系统提示安装成功)，win+r打开regedit，注册表定位到`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts`删除带MSPGothic字样的字体项目值再尝试安装SExtract的MSPGothic字体文件，win10/11大概率会出现这问题

        *   本仓库`JIS字体批量替换`文件夹提供ＭＳ Pゴシック和ＭＳ ゴシック字体文件(是同一个字体文件，只是字体属性不一样)
---
