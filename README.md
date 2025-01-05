# Livemaker翻译、中文汉化教程

一些自己汉化Livemaker的经验，个人只修改了剧情文本对话，其它的如图片、选项没改

需求：
- python基本知识
- 正则表达式
- json语法
- csv基本知识

最近有热心网友也编写了自己的经验，我感觉写的非常好比我的技术力强多了，不过因为它是fork的无法直接搜索到，因此在这里指路方便大家学习汉化

https://github.com/allrobot/Livemaker-chinese-tl/tree/main

非常感谢这位网友愿意分享自己的经验，也让我学习到原来我放弃的方案是如何实现的。

首先，我们使用的工具如下：

（1）Pylivemaker，来自https://github.com/pmrowla/pylivemaker ；

（2）FontCreator，非开源软件；

（3）Locale.Emulator，来自https://github.com/xupefei/Locale-Emulator 

（4）SExtract，来自https://github.com/satan53x/SExtractor ；

（5）AiNiee或GalTransl，来自https://github.com/NEKOparapa/AiNiee 和 https://github.com/cx2333-gt/GalTransl ；

（6）UniversalInjectorFramework，来自https://github.com/AtomCrafty/UniversalInjectorFramework

Pylivemaker是韩国人开发用于解密livemaker引擎资料的工具，依赖Python实现解密
根据pylivemaker作者要求Python>=3.8，可通过Conda安装，或https://www.python.org/downloads/ 下载最新版本

>提醒：SExtract要求Python>=3.9版本

```CMD
pip install pylivemaker
```

Locale.Emulator点Release发行版下载一个，其它SExtract、AiNiee或GalTransl需要git clone
```CMD
git clone git@github.com:satan53x/SExtractor.git
cd SExtractor
安装依赖.bat
运行.bat
```

其他软件自行获取安装包安装即可


## 第一步

据[pylivemaker文档](https://pylivemaker.readthedocs.io/en/latest/usage.html4) 说明，win+r或win+q搜索cmd，跳转到game所在的路径

```CMD
cd /d "D:\livemaker游戏exe所在的路径"
lmar x game.exe -o 解包文件夹名（随意命名）
```


## 第二步

我们在解包出来的文件中，寻找剧本(scenario
)，往往是解包目录下最大的lsb文件，使用pylivemaker将其转换为csv，例如我的剧本lsb是00000033.lsb，那么打开cmd，使用以下命令即可：

```CMD
lmlsb extractcsv --encoding=utf-8-sig 00000033.lsb 00000033.csv
```

即可生成00000033.csv文件，如果用txt文件打开，可以了解CSV最基本的结构

## 第三步

通过SExtract提取CSV的文本转为JSON文件，JSON用于给两个AI翻译软件方便读取翻译的

当然，用Translater++也可以提取CSV文本，但是个人觉得这个功能不怎么靠谱，解析一个CSV文件居然缺斤少两的，读取的CSV少了几十行

SExtract引擎选JSON，规则选CSV，修改为：

```
22_search=^([\s\S]+)
extraData=^Original text$
writeOffset=1
```

writeOffset=1是当前单元格右侧1列中写入，正好是`Original text`单元格右边的`Translated text`
根据需要增删改regex过滤提取文本，比如提取`「`和`」`之间的文本

提取后生成`ctrl`和`new`文件夹，`ctrl`包含提取的文本json，如果用AiNiee工具选择该文件进行翻译，保存读取都选同一个ctrl路径，翻完了AiNiee新建`transDic.output_transDic.json.json`文件，将把文件修改至`transDic.json`覆盖原文件(注意备份)，然后在SE工具中点注入按钮，它给new路径下生成新的csv文件，把这个csv文件放回原来的`解包文件夹名`目录覆盖原csv文件(注意备份)


## 第四步

翻译……

翻译操作自行参阅AI软件的文档，个人建议云大模型翻译，因为本地模型跑的很慢，翻译1mb文本要翻译一整天

如果你有一块好显卡，保证显存20G~50G，那么可以通过CausalLM-35B或Sakura部署本地大模型翻译

翻译完成后，请在SExtract设置勾选JIS注入，确保生成的json全是日文(CP932字符)，避免注入时报错，比如cmd的英文报错大量不属于CP932的字符


## 第五步

当你完成了汉化工作：

```CMD
lmlsb insertcsv --encoding=utf-8-sig 00000033.lsb 00000033.csv
```

>如果没勾选`生成UniversalInjector的JIS替换配置`，直接把翻译文本的csv转为lsb文件，cmd会报错一大堆信息，说有大量不属于CP932的字符
>
>因为pylivemaker的lmlsb只支持JIS编码导入（lm引擎仅支持cp932代码页），有3种办法来解决：
>https://github.com/satan53x/SExtractor/blob/552ce5dc254c6623d5b21b928486c48d90fa32fd/document/1_JIS%E6%9B%BF%E6%8D%A2%E5%AE%9E%E4%BE%8B_Alicesoft.MD?plain=1#L81C1-L89C28
>
>参考资料：https://github.com/satan53x/SExtractor/blob/552ce5dc254c6623d5b21b928486c48d90fa32fd/document/1_JIS%E6%9B%BF%E6%8D%A2%E5%AE%9E%E4%BE%8B_Alicesoft.MD
>
>上面提到的SE工具，在设置勾选`生成UniversalInjector的JIS替换配置`，把CSV文件种gbk编码的字体转为JIS字体就能正常导入了


## 第六步

00000033.lsb和xxx.exe需要在同一个目录下
```
lmpatch some.exe 00000001.lsb
```

生成exe后，用Locale.Emulator打开游戏发现日文字符修改成功了，只需要做下面任意字体方案即可，其中3.（2） 的方案最快捷

1. 使用UIF方案

参考链接：https://github.com/AtomCrafty/UniversalInjectorFramework

或直接下载https://github.com/satan53x/SExtractor/tree/552ce5dc254c6623d5b21b928486c48d90fa32fd/tools/UniversalInjectorFramework 事先编译好的dll文件，具体原理是伪装系统dll，让exe优先加载dll，dll就能加载createFont相关的函数替换为简体

想确定游戏有没有加载dll或dll捕获到游戏的字体函数，`uif_config.json`的allocate_console修改为true，启用游戏后会调用CMD打印日志

>任选一个dll，我这里用的winmm.dll

SE在设置勾选`生成UniversalInjector的JIS替换配置`后，ctrl会生成`uif_config.json`文件，把json和dll移至游戏根目录，打开json启用配置（配置自己弄）

2. UIF启用字体更换

配置文件通过启用font_manager自行加载

3. 安装字体

部分游戏UIF可能无法显示，以ストッピング!!!2 ロ○っ子図書館編游戏为例，UIF配置试了遍，无论转不转区都是显示gbk乱码

这时候需要替换字体方案：

（1） 我采用的是替换字体方案，Livemaker一般默认调用MS Gothic字体，因此我们只需要更改MS Gothic，将CP932中存在的不怎么使用的字符替换掉，即可让Livemaker显示我们需要的字符。

CP932涵盖的字符在此查阅：https://uic.win/zh-hant/charset/show/cp932/

在这里，我提供一下我修改过的Livemaker字体，取自思源黑体，以及Livemaker替换表，如果你汉化的内容有新的字符需要导入，则自己使用FontCreator替换即可。

注意：在使用我提供的Livemaker替换表之前，应先把文本简转繁，因为在我修改的字体中，简繁体不同的字体已经被合并到一起，统一显示为简体字形，CP932中的繁体字多于简体字，因此也建议尽量使用繁体文本，减少需要导入的新字符。

>如果不想使用FontCreator手动更换字体，可以使用otfcc提供的工具批量更换字体，详细参见本仓库目录的`JIS字体批量替换`的脚本`font_CN_JP.py`

（2） 安装https://github.com/satan53x/SExtractor/tree/552ce5dc254c6623d5b21b928486c48d90fa32fd/tools/Font 提供的ttf文件，只要是SE转换的JIS字体，转区启动游戏均为能显示中文字体

>如果字体安装后还是没办法看到中文
>① 重启电脑了吗？ 
>② 在`解包文件夹名`导出文件夹中，[cmd批量执行](https://github.com/allrobot/Translator-_and_others_script/tree/main/%E8%84%9A%E6%9C%AC/livemaker%E5%BC%95%E6%93%8E) `lmlsb dump xxx.lsb > xxx.lsb.txt`，打开notepad++启用文件查找`font`看看是lm引擎用的哪个字体文件，比如ストッピング!!!2 ロ○っ子図書館編游戏加载的是ＭＳ Pゴシック(MSPGothic)字体，并非ＭＳ ゴシック(MSGothic)字体，打开FontCreator把satan53x提供的WenQuanYi_msgothic.otf字体属性修改成ＭＳ Pゴシック
>③ 部分字体没有显示为中文，打开FontCreator搜目标JIS字体，把另一个黑体文件中的简体字复制黏贴到搜到的JIS字体，或使用`font_CN_JP.py`要求的`subs_cn_jp.json`字典添加{"要求显示的中文x":"游戏显示的日文x"}，导出为ttf然后安装重启PC，但这情况不太可能出现
>④ 系统的MSPGothic并没有被SExtract提供的字体文件覆盖掉(即使系统提示安装成功)，win+r打开regedit，注册表定位到`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts`删除带MSPGothic字样的字体项目值再尝试安装SExtract的MSPGothic字体文件，win10/11大概率会出现这问题

>这里仓库`JIS字体批量替换`文件夹提供ＭＳ Pゴシック和ＭＳ ゴシック字体文件(是同一个字体文件，只是字体属性不一样)

