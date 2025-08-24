from typing import Literal, Union
from dataclasses import dataclass

from PySide6.QtGui import QImage

# 1. 纯文本项目记录(id == 0)
# 2. 文件类存路径(目前只可以是本地的文件，但是文件可以多个)，多文件情况最大支持一共100MB的文件(id == 1)
# 3. 只保存像素的图片类虽然属于文件，但是不会存储路径，因此使用QImage存储临时信息(id == 2)
# 4. 富文本，像Word复制下来的纯文本也会被保存为格式(id == 3)
@dataclass
class DataItem:
    content : Union[str, list[str], tuple[str, QImage]]
    id : Literal[0, 1, 2, 3]

# UI统一混入协议
class RuleMixin(object):
    # UI初始化
    def __setUI(self) -> None: pass
    # 连接信号和槽
    def __link(self) -> None: pass

