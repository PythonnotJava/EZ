import json5
from pathlib import Path
from mimetypes import guess_type
from PySide6.QtGui import QFont

JsonCfg = str(Path(__file__).parent / 'assets/cfg.json5')

try:
    f = open(JsonCfg, 'r', encoding='utf-8')
    cfgReader : dict = json5.load(f)
    f.close()
    print('Suc')
except ValueError:
    print('Fail')
    cfgReader = {
        'shadow' : {
            'open' : True,
            'rgba' : [110, 110, 0, 80]
        },
        'MAXITEMCOUNTS' : 15,
        'PURETEXTFONT' : {
            'pointSize' : 12
        },
        'SINGLEFILEPATHFONT' : {
            'pointSize' : 12
        },
        'MULTEFILEPATHFONT' : {
            'pointSize' : 10
        },
        'PIXMAPFONT' : {
            'pointSize' : 20
        },
        'CARDFIXHEIGHT' : 80,
        'TOTALFILESMAXSUPPORT' : 1073741824,
        'SupportImageType' : ["png", "jpeg", "jpg", "gif", "bmp", "webp"],
        'ItemCardStyleQSS' : "background: white;border-radius: 10px",
        'shortcut' : ['Option', 'V']
    }

cfgReaderPretty : str = json5.dumps(cfgReader, indent=4, ensure_ascii=False)

# 全局配置
# 剪切板列表最大项目数——越大想要记录的东西越多，建议范围10～30
MAXITEMCOUNTS : int = cfgReader.get('MAXITEMCOUNTS', 15)
if not (10 <= MAXITEMCOUNTS <= 30):
    MAXITEMCOUNTS = 15
# 纯文本模式字体
PURETEXTFONT = QFont()
PURETEXTFONT.setPointSize(cfgReader.get('PURETEXTFONT', {'pointSize' : 12}).get('pointSize', 12))
# 单文件模式路径字体
SINGLEFILEPATHFONT = QFont()
SINGLEFILEPATHFONT.setPointSize(cfgReader.get('SINGLEFILEPATHFONT', {'pointSize' : 12}).get('pointSize', 12))
# 多文件模式路径字体
MULTEFILEPATHFONT = QFont()
MULTEFILEPATHFONT.setPointSize(cfgReader.get('MULTEFILEPATHFONT', {'pointSize' : 10}).get('pointSize', 10))
# 像素图片子体
PIXMAPFONT = QFont()
PIXMAPFONT.setPointSize(cfgReader.get('PIXMAPFONT', {'pointSize' : 20}).get('pointSize', 20))
# 卡片固定高度
CARDFIXHEIGHT : int = cfgReader.get('CARDFIXHEIGHT', 80)
if not (50 <= CARDFIXHEIGHT <= 100):
    CARDFIXHEIGHT = 80
# 文件总大小上限
TOTALFILESMAXSUPPORT : int = cfgReader.get('TOTALFILESMAXSUPPORT', 1073741824)
if not (0 <= TOTALFILESMAXSUPPORT <= 1073741824):
    TOTALFILESMAXSUPPORT = 1073741824
# 文件类型是图片的时候，支持哪些格式（这些格式都是QPixmap能画的）
isSupportImageType = lambda name: (
    (mime := guess_type(name)[0]) is not None
    and mime.startswith("image/")
    and mime.split("/")[1].lower() in ["png", "jpeg", "jpg", "gif", "bmp", "webp"]
)
# 是否开启模糊效果以及颜色
_shadow = cfgReader.get('shadow', {'open' : True, 'rgba' : [110, 110, 0, 80]})
shadowOpen : bool = _shadow.get('open', True)
shadowColor : list[int] = _shadow.get('rgba', [110, 110, 0, 80])
# 卡片样式
CARDSTYLE : str = cfgReader.get('ItemCardStyleQSS', '')

def writeBack(data : dict) -> None:
    with open(JsonCfg, 'w', encoding='utf-8') as fi:
        json5.dump(data, fi, indent=4,)
        fi.close()

def judgeIsDict(data : str) -> tuple[bool, dict]:
    get = json5.parse(data)
    return get[0] is not None, get[0]
