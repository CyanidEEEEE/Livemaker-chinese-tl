# Livemaker翻译、中文汉化教程

    为了汉化黑礁2、3，研究Livemaker已经很久了，中文互联网上残留的几篇教程，存在着诸多问题，例如只能解密而不能加密回去，只知道如何打开剧本文件修改，却因为他们自己并没有实际汉化，而根本不知道livemaker只能使用CP932编码的事实。

今天，为了解决这些漫长的遗留问题，我将介绍自己汉化Livemaker的经验。

首先，我们使用的工具如下：

（1）Pylivemaker，来自https://github.com/pmrowla/pylivemaker ；

（2）FontCreator，非开源软件；

（3）openoffice或libreoffice，来自https://www.libreoffice.org/ ；

（4）Locale.Emulator，来自https://github.com/xupefei/Locale-Emulator 
      
（5）GraphicsGale，来自https://graphicsgale.com/us/download.html ；


我们首先要做的就是，安装上述软件，安装livemaker需要安装最新的python，然后进入cmd使用pip install pylivemaker命令，安装完毕。

其他软件自行获取安装包安装即可。


## 第一步

下面我们要做的是解包，解包只需要使用pylivemaker，在需要解包的游戏exe的目录下打开cmd，使用（game为游戏exe名称，而后的game_files随意命名）

<p align="center">lmar x game.exe -o game_files</p>




## 第二步

我们在解包出来的文件中，寻找剧本，往往是解包目录下最大的lsb文件，使用pylivemaker将其转换为csv，例如我的剧本lsb是00000033.lsb，那么打开cmd，使用以下命令即可：

<p align="center">lmlsb extractcsv --encoding=utf-8-sig 00000033.lsb 00000033.csv</p>

我们将得到00000033.csv，用openoffice或libreoffice使用以下参数打开：
      
![image](https://github.com/CyanidEEEEE/Livmaker-chinese-tl/blob/main/1.png)

即可看到类似excel排列的剧本文件，我们需要汉化的内容只需要对照原文格式填入Translated text即可，注意，换行符也应对齐，在编辑时按下ctrl+enter即可输入。


## 第三步

当你完成了汉化工作，我们直接使用：

<p align="center">lmlsb insertcsv --encoding=utf-8-sig 00000033.lsb 00000033.csv</p>

尝试将翻译文本导入，会发现提示错误，有大量不属于CP932的字符，因此接下来，我们要处理这个问题。

我采用的是替换字体方案，Livemaker一般默认调用MS Gothic字体，因此我们只需要更改MS Gothic，将CP932中存在的不怎么使用的字符替换掉，即可让Livemaker显示我们需要的字符。

CP932涵盖的字符在此查阅：https://uic.win/zh-hant/charset/show/cp932/

在这里，我提供一下我修改过的Livemaker字体，取自思源黑体，以及Livemaker替换表，如果你汉化的内容有新的字符需要导入，则自己使用FontCreator替换即可。

注意：在使用我提供的Livemaker替换表之前，应先把文本简转繁，因为在我修改的字体中，简繁体不同的字体已经被合并到一起，统一显示为简体字形，CP932中的繁体字多于简体字，因此也建议尽量使用繁体文本，减少需要导入的新字符。


## 第四步

我们搞定文本，则需要更改UI，Livemaker的图片格式很特别，由Humanbalance的软件GraphicsGale才能转换，我们使用这个软件，要注意，他转换出来的PNG带有阿尔法通道，往往难以编辑，因此我建议使用Image - Duplicate Alpha Channel的方式，将阿尔法通道分离，然后再导出编辑或者导出后在GraphicsGale编辑，之后在使用Image - Make Alpha Channel参数选择Luminance和之前分离的图片，即可恢复阿尔法通道。


## 第五步

接下来，我们只需要处理一些琐碎的东西即可，例如选项文本，往往不会在导出的csv中，我们需要使用：

<p align="center">lmlsb dump --encoding=utf-8 00000033.lsb --mode xml --output-file 00000033.xml</p>

将其转换成人类可阅读的xml格式，然后找到相应的位置，对着文本所在的LineNo="XXX"，使用以下命令：

<p align="center">lmlsb edit 00000033.lsb XXX</p>

即可编辑该处，除了文本，其余尽量不要修改。



## 第六步

修改一些参数，我个人也没有深入研究，不过更改字体显示的参数在我所汉化的游戏中，位于メッセージボックス作成.lsb，因此我们按照第五步的方法，使用：

<p align="center">lmlsb dump --encoding=utf-8 メッセージボックス作成.lsb --mode xml --output-file メッセージボックス作成.xml</p>

然后自行查看文本，按照第五步的方法更改调试即可。


## 第七步
 
我不推荐将游戏完整放出的方式，因此推荐利用Livemaker优先调用外面目录文件的特性，放出补丁，只要将需要更改的文件放出即可，然后让使用者将原游戏exe放在补丁目录下，即可使用。
