import json
import subprocess
import sys

FontSrc = 'WenQuanYi.ttf'
SubsJson = 'subs_cn_jp.json'
Reverse = True 

#字典键值交换位置
#批量把日文字体文件中的日文替换为中文字体

def main():
    if len(sys.argv) >= 2:
        fnt = sys.argv[1]
    else:
        fnt = FontSrc
    
    obj = json.loads(subprocess.check_output(('otfccdump.exe', '-n', '0', '--hex-cmap', '--no-bom', fnt)))

    with open(SubsJson, encoding='utf-8') as f:
        print('读入Json', SubsJson)
        data:dict = json.load(f)
        #键值互换
        if Reverse:
            newDic = {}
            for key, value in data.items():
                if value in newDic:
                    print('新Key已存在', value)
                else:
                    newDic[value] = key
            data = newDic
        #替换
        for key, value in data.items():
            if key == value:
                continue
            s = f'U+{ord(key):04X}'
            j = f'U+{ord(value):04X}'
            try:
                obj['cmap'][s] = obj['cmap'][j]
            except:
                print('字体中不存在:', key, value)
        #更改定义
        #changeDef(obj)
    #注入到 xxx_替换后.ttf 字体文件
    subprocess.run(['otfccbuild.exe', '-O3', '-o', '%s_替换后.ttf' % fnt[0:fnt.rfind('.')]], input=json.dumps(obj), encoding='utf-8')
    print(f'已将{FontSrc}字体中的日文替换为中文，可以使用该该文件了')


if __name__ == '__main__':
    main()