# Livemaker翻译、中文汉化教程

为了汉化黑礁2、3，研究Livemaker已经很久了，中文互联网上残留的几篇教程，存在着诸多问题，例如只能解密而不能加密回去，只知道如何打开剧本文件修改，却因为他们自己并没有实际汉化，而根本不知道livemaker只能使用CP932编码的事实。

今天，为了解决这些漫长的遗留问题，我将介绍自己汉化Livemaker的经验。

首先，我们使用的工具如下：

（1）Pylivemaker，来自https://github.com/pmrowla/pylivemaker ；

（2）FontCreator，非开源软件；

（3）openoffice或libreoffice，来自https://www.libreoffice.org/ ；

（4）Locale.Emulator，来自https://github.com/xupefei/Locale-Emulator 
      
（5）GraphicsGale，来自https://graphicsgale.com/us/download.html ；

（6）SExtract，来自https://github.com/satan53x/SExtractor ；

（7）AiNiee或GalTransl，来自https://github.com/NEKOparapa/AiNiee 和 https://github.com/cx2333-gt/GalTransl ；

（8）UniversalInjectorFramework，来自https://github.com/AtomCrafty/UniversalInjectorFramework

（9）otfccbuild或otfccdump，来自https://github.com/caryll/otfcc


我们首先要做的就是，安装上述软件，安装livemaker需要安装最新的python，然后进入cmd使用pip install pylivemaker命令，安装完毕。

其他软件自行获取安装包安装即可。


## 第一步

下面我们要做的是解包，解包只需要使用pylivemaker，在需要解包的游戏exe的目录下打开cmd，使用（game为游戏exe名称，而后的game_files随意命名）

```CMD
lmar x game.exe -o game_files
```


## 第二步

我们在解包出来的文件中，寻找剧本，往往是解包目录下最大的lsb文件，使用pylivemaker将其转换为csv，例如我的剧本lsb是00000033.lsb，那么打开cmd，使用以下命令即可：

```CMD
lmlsb extractcsv --encoding=utf-8-sig 00000033.lsb 00000033.csv
```

有2种办法汉化：

1. 我们将得到00000033.csv，用openoffice或libreoffice使用以下参数打开：
      
![image](https://github.com/CyanidEEEEE/Livmaker-chinese-tl/blob/main/1.png)

即可看到类似excel排列的剧本文件，我们需要汉化的内容只需要对照原文格式填入Translated text即可，注意，换行符也应对齐，在编辑时按下ctrl+enter即可输入。

2. 通过SExtract提取CSV的文本，使用[AiNiee](https://github.com/NEKOparapa/AiNiee) 或 [GalTransl](https://github.com/cx2333-gt/GalTransl) AI翻译工具汉化

把CSV文件移到单独的目录

SExtract引擎选JSON，规则选CSV，修改为：
```
22_search=^([\s\S]+)
extraData=^Original text$
writeOffset=1
```
writeOffset=1是当前单元格右侧1列中写入，正好是`Original text`单元格右边的`Translated text`
根据需要增删改regex过滤提取文本，比如提取`「`和`」`之间的文本
提取后生成ctrl和new文件夹，ctrl就存放提取后的文本json，以AiNiee工具为例，保存读取都选同一个ctrl路径，翻完了把新创建的`transDic.output_transDic.json.json`文件修改至`transDic.json`，然后在SE工具中给new文件生成新的csv文件，最后把csv文件放回原来的`game_files`目录就行


## 第三步

当你完成了汉化工作，我们直接使用：

```CMD
lmlsb insertcsv --encoding=utf-8-sig 00000033.lsb 00000033.csv
```

尝试将翻译文本导入，会发现提示错误，有大量不属于CP932的字符，因此接下来，我们要处理这个问题。

因为pylivemaker的lmlsb只支持JIS编码导入（lm引擎仅支持cp932代码页），有3种办法来解决：
https://github.com/satan53x/SExtractor/blob/552ce5dc254c6623d5b21b928486c48d90fa32fd/document/1_JIS%E6%9B%BF%E6%8D%A2%E5%AE%9E%E4%BE%8B_Alicesoft.MD?plain=1#L81C1-L89C28

参考资料：https://github.com/satan53x/SExtractor/blob/552ce5dc254c6623d5b21b928486c48d90fa32fd/document/1_JIS%E6%9B%BF%E6%8D%A2%E5%AE%9E%E4%BE%8B_Alicesoft.MD

上面提到的SE工具，在设置勾选`生成UniversalInjector的JIS替换配置`，把CSV文件种gbk编码的字体转为JIS字体就能正常导入了

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
>② 在game_files导出文件夹中，[cmd批量执行](https://github.com/allrobot/Translator-_and_others_script/tree/main/%E8%84%9A%E6%9C%AC/livemaker%E5%BC%95%E6%93%8E) `lmlsb dump xxx.lsb > xxx.lsb.txt`，打开notepad++启用文件查找`font`看看是lm引擎用的哪个字体文件，比如ストッピング!!!2 ロ○っ子図書館編游戏加载的是ＭＳ Pゴシック(MSPGothic)字体，并非ＭＳ ゴシック(MSGothic)字体，打开FontCreator把satan53x提供的WenQuanYi_msgothic.otf字体属性修改成ＭＳ Pゴシック
>③ 部分字体没有显示为中文，打开FontCreator搜目标JIS字体，把另一个黑体文件中的简体字复制黏贴到搜到的JIS字体，或使用`font_CN_JP.py`要求的`subs_cn_jp.json`字典添加{"要求显示的中文x":"游戏显示的日文x"}，导出为ttf然后安装重启PC

>这里仓库`JIS字体批量替换`文件夹提供ＭＳ Pゴシック和ＭＳ ゴシック字体文件(是同一个字体文件，只是字体属性不一样)




## 第四步

我们搞定文本，则需要更改UI，Livemaker的图片格式很特别，由Humanbalance的软件GraphicsGale才能转换，我们使用这个软件，要注意，他转换出来的PNG带有阿尔法通道，往往难以编辑，因此我建议使用Image - Duplicate Alpha Channel的方式，将阿尔法通道分离，然后再导出编辑或者导出后在GraphicsGale编辑，之后在使用Image - Make Alpha Channel参数选择Luminance和之前分离的图片，即可恢复阿尔法通道。


## 第五步

接下来，我们只需要处理一些琐碎的东西即可，例如选项文本，往往不会在导出的csv中，我们需要使用：

```CMD
lmlsb dump --encoding=utf-8 00000033.lsb --mode xml --output-file 00000033.xml
```

将其转换成人类可阅读的xml格式，然后找到相应的位置，对着文本所在的LineNo="XXX"，使用以下命令：

```CMD
lmlsb edit 00000033.lsb XXX
```

即可编辑该处，除了文本，其余尽量不要修改。



## 第六步

修改一些参数，我个人也没有深入研究，不过更改字体显示的参数在我所汉化的游戏中，位于メッセージボックス作成.lsb，因此我们按照第五步的方法，使用：

```CMD
lmlsb dump --encoding=utf-8 メッセージボックス作成.lsb --mode xml --output-file メッセージボックス作成.xml
```

然后自行查看文本，按照第五步的方法更改调试即可。


## 第七步

lsb和exe需要在同一个目录下
```
lmpatch some.exe 00000001.lsb
```
 
我不推荐将游戏完整放出的方式，因此推荐利用Livemaker优先调用外面目录文件的特性，放出补丁，只要将需要更改的文件放出即可，然后让使用者将原游戏exe放在补丁目录下，即可使用。
