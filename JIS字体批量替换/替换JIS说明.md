## 说明

font_CN_JP.py使用的字典为src下的subs_cn_jp.json。

原理：通过字典，将subs_cn_jp.json中的日文字体替换为汉字然后导入到新的字体文件中（但并不是标准的日繁对应关系）
安装替换后的字体文件，游戏中的JIS字体将显示为对应的简体中文，或者使用UIF的`font_manager`加载（即使函数不能hook也可以加载）

>如果游戏不支持修改字体时，需要安装修改后的字体

 ## JIS替换 
 
使用font_CN_JP.py批量替换字体文件中的日文为中文，参考`subs_cn_jp.json`字典
替换后的字体文件通过`UIF`的hook或者ttf/otf字体把对应的日文还原为简体输出

* 还原方法1：UIF的`character_substitution`模块hook系统函数

把dll和uif_config.json放在Game.exe根目录中，自行修改uif_config.json配置文件启动模块

* 还原方法2：使用JIS替换字典对应的ttf字体，通过UIF的`font_manager`模块加载

把修改后的字体放在游戏根目录，`resource_files`填入该字体文件的路径，`enable`改为true

* 还原方法3：不需要UIF，直接安装替换后的ttf字体

使用SExtract工具勾选设置的`生成UniversalInjector的JIS替换配置`批量替换简体为JIS字体注入到游戏中，然后安装WenQuanYi_msgothic.otf和MSPGothic-Regular.ttf文件，游戏则显示对应的中文，如果没显示，请重启电脑

## 字体属性修改

如果游戏不能通过游戏内选择或修改exe更改字体，则需要用FontCreator修改字体属性，以替换系统自带的日文字体：

* 字体系：`MS Gothic`
* 字体系：`ＭＳ ゴシック`
* 唯一标识：`Microsoft:ＭＳ ゴシック`
* 匹配规格：`2-11-6-9-7-2-5-8-2-4` `2-2-4-0-0-0-0-0-0-0`

## 文件

* 原字体：`WenQuanYi.ttf`（WenQuanYi Micro Hei）
* 替换后：`WenQuanYi_CNJP.ttf`（WenQuanYi）
* 字体名MS Gothic修正后：`WenQuanYi_msgothic.otf`（ＭＳ ゴシック）
* 字体名MS Gothic修正后：`MSPGothic-Regular.ttf`（ＭＳ Pゴシック）

## 工具

otfcc: https://github.com/caryll/otfcc

FontCreator: 非开源