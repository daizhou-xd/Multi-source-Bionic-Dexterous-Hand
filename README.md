# Multi-source-Bionic-Dexterous-Hand

多源仿生灵巧手 - 螺旋机器人设计工具

## 📦 环境配置

### 前置要求

- [Anaconda](https://www.anaconda.com/) 或 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Python 3.11 (通过 conda 自动安装)

### 创建环境

```bash
conda env create -f environment.yml
```

这将创建名为 `bionic-hand` 的环境，并安装所有依赖包。

## 🚀 快速开始

创建环境后，直接运行：

```bash
conda run -n bionic-hand python design_software\design_software.py
```

就这么简单！无需激活环境，无需管理员权限。

详细说明请参考：[如何运行.md](如何运行.md)

## 📚 依赖包

- Python 3.11
- PySide6 (Qt6 GUI框架)
- matplotlib (2D绘图)
- cadquery (CAD建模)
- numpy (数值计算)

## 💡 常见问题

### 运行时提示 `ModuleNotFoundError: No module named 'PySide6'`？

请使用 conda run 命令运行：
```bash
conda run -n bionic-hand python design_software\design_software.py
```

### 想要更灵活的使用方式？

也可以在 VSCode 中选择 `bionic-hand` 环境的 Python 解释器，然后按 F5 运行。

更多问题请查看 [如何运行.md](如何运行.md)

## 📝 License

待补充
