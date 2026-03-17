# 命令行待办事项管理器

一个功能完整的Python命令行待办事项管理器，支持任务管理、优先级设置、截止日期提醒和数据持久化。

## ✨ 功能特性

- ✅ **任务管理**：添加、查看、编辑、删除、完成任务
- 🎯 **优先级系统**：高(🔴)、中(🟡)、低(🟢)三个优先级
- 📅 **截止日期**：支持设置截止日期，自动计算逾期
- 🔍 **智能搜索**：按关键词搜索任务标题和描述
- 📊 **数据统计**：任务完成率、逾期任务统计
- 💾 **数据持久化**：使用JSON文件自动保存数据
- 📤 **导入导出**：支持任务列表的导入导出
- 🎨 **美观界面**：彩色图标和清晰的显示格式

## 🚀 快速开始

### 安装
```bash
# 克隆仓库
git clone https://github.com/mubaihe25/todo-manager.git
cd todo-manager

# 运行（无需安装依赖，使用Python 3.7+）
python todo_manager.py
```

### 基本使用
1. 运行程序：`python todo_manager.py`
2. 根据菜单提示选择操作
3. 任务数据会自动保存在 `todos.json` 文件中

## 📋 使用示例

```
📋 命令行待办事项管理器
==================================================
1. 📝 添加新任务
2. 👁️  查看所有任务
3. 🔍 搜索任务
4. ✅ 标记完成/未完成
5. ✏️  编辑任务
6. 🗑️  删除任务
7. 📊 显示统计
8. 💾 导出任务
9. 📂 导入任务
0. 🚪 退出
--------------------------------------------------
请选择: 1

📝 添加新任务
任务标题: 完成Python项目
任务描述（可选）: 为GitHub创建一个展示项目
优先级 (1-高, 2-中, 3-低) [3]: 1
截止日期 (YYYY-MM-DD，可选): 2026-03-20
✅ 已添加任务: 完成Python项目
```

## 🏗️ 项目结构

```
todo-manager/
├── todo_manager.py     # 主程序文件
├── todos.json         # 任务数据文件（自动生成）
├── requirements.txt   # 项目依赖
└── README.md         # 项目说明
```

## 💻 技术栈

- **Python 3.7+** - 编程语言
- **标准库** - 仅使用Python内置库：
  - `dataclasses` - 数据类
  - `json` - JSON序列化
  - `datetime` - 日期时间处理
  - `os` - 文件系统操作
  - `sys` - 系统相关功能

## 🔧 核心功能实现

### 1. 数据模型
使用`dataclasses`定义`TodoItem`类，包含任务的所有属性。

### 2. 数据持久化
任务数据自动保存到JSON文件，程序重启后数据不丢失。

### 3. 用户界面
简洁的命令行菜单，支持键盘中断和错误处理。

### 4. 任务提醒
自动检测逾期任务并在启动时显示提醒。

## 🧪 运行测试

```bash
# 直接运行主程序
python todo_manager.py

# 或者给执行权限后直接运行（Linux/Mac）
chmod +x todo_manager.py
./todo_manager.py
```

## 📁 文件说明

- **todos.json**: 任务数据存储文件（首次运行后自动生成）
- **todo_manager.py**: 主程序文件，包含所有功能
- **todos_export.json**: 导出任务时的默认文件名

## 🚀 进阶功能建议

想要扩展这个项目？可以考虑：

1. **添加分类标签**：支持为任务添加标签进行分类
2. **重复任务**：支持每日/每周重复任务
3. **数据加密**：对todos.json进行加密保护隐私
4. **云端同步**：支持多设备同步
5. **命令行参数**：支持命令行直接操作任务
6. **图形界面**：使用Tkinter/PyQt添加GUI

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目基于MIT许可证开源。

## 👤 作者

你的名字
- GitHub: [@mubaihe25](https://github.com/mubaihe25)
- 项目链接: [todo-manager](https://github.com/mubaihe25/todo-manager)

---

⭐️ 如果这个项目对你有帮助，请点个Star！
