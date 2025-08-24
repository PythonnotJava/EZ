# 开机启动设定，仅支持Mac OS，原理是注册plist文件（官方推荐的）
import os
import sys
import plistlib
import logging

logger = logging.getLogger(__name__)

APPLICATION_NAME = "EZ"
APPLICATION_MACOS_SIGNATURE = "local.ez"
PLIST_FILENAME = f"{APPLICATION_MACOS_SIGNATURE}.{APPLICATION_NAME}.plist"

class MacStartupOnBoot:

    @staticmethod
    def is_enabled() -> bool:
        autostartDir = os.path.join(
            os.path.expanduser('~'), 'Library', 'LaunchAgents'
        )
        plistPath = os.path.join(autostartDir, "local.ez.EZ.plist")
        return os.path.exists(plistPath)

    @staticmethod
    def on_():
        autostartDir = os.path.join(
            os.path.expanduser('~'), 'Library', 'LaunchAgents'
        )

        try:
            os.makedirs(autostartDir, exist_ok=True)
        except Exception as e:
            logger.error(f"创建 LaunchAgents 目录失败: {e}")
            return False

        plistData = {
            "Label": f"{APPLICATION_MACOS_SIGNATURE}.{APPLICATION_NAME}",
            "ProgramArguments": [sys.argv[0]],   # 程序路径
            "RunAtLoad": True,                   # 开机自启
        }

        try:
            with open(os.path.join(autostartDir, PLIST_FILENAME), "wb") as file:
                plistlib.dump(plistData, file)
        except Exception as e:
            logger.error(f"写入 plist 失败: {e}")
            return False
        else:
            logger.info("macOS StartupOnBoot 已开启")
            return True

    @staticmethod
    def off_():
        autostartDir = os.path.join(
            os.path.expanduser('~'), 'Library', 'LaunchAgents'
        )
        plistPath = os.path.join(autostartDir, PLIST_FILENAME)

        try:
            os.remove(plistPath)
        except FileNotFoundError:
            logger.info("plist 文件不存在，视为已关闭")
            return True
        except Exception as e:
            logger.error(f"删除 plist 失败: {e}")
            return False
        else:
            logger.info("macOS StartupOnBoot 已关闭")
            return True

def setup_logging():
    log_dir = os.path.expanduser("~/Library/Logs/EZ")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "EZ.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()  # 同时输出到控制台
        ]
    )
    logging.info("EZ 日志系统初始化完成")