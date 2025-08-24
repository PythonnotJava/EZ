# EZ

EZ（类似Easy的发音）是一款类似Windows ClipBoard的Mac剪切板软件，支持文本和文件（可以多文件）的实时记录、历史项点击覆盖当前项的功能。EZ采用PySide6+MIT许可证。

- EZ被关闭后不会立马退出，而是放到系统托盘。
- EZ可以设置开启启动。软件第一次初始化的时候，不会设置重新启动，需要自己去到系统托盘图标感受一下。
- EZ没有实现简单的配置系统，只保留了原始的修改文本方法，修改后重启则同步。配置的相关实现查看：[EZCfg.py](EZCfg.py)


## 打包命令
```text
nuitka EZ.py \
  --standalone \
  --enable-plugin=pyside6 \
  --macos-create-app-bundle \
  --macos-app-icon=assets/logo.ico \
  --include-data-dir=assets=assets \
  --output-dir=dist


hdiutil create -volname "EZApp" \
  -srcfolder "dist/EZ.app" \
  -ov -format UDZO "dist/EZ.dmg"

```