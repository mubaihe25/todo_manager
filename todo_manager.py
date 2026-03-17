#!/usr/bin/env python3
"""
命令行待办事项管理器
功能：添加、查看、完成、删除任务，设置优先级和截止日期
数据使用JSON持久化保存
"""
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional
import sys

@dataclass
class TodoItem:
    """待办事项数据类"""
    id: int
    title: str
    description: str = ""
    priority: int = 3  # 1-高, 2-中, 3-低
    due_date: Optional[str] = None
    completed: bool = False
    created_at: str = ""
    
    def __post_init__(self):
        """初始化后自动设置创建时间"""
        if not self.created_at:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def display(self, detailed: bool = False) -> str:
        """格式化显示任务信息"""
        status = "✓" if self.completed else "○"
        priority_map = {1: "🔴 高", 2: "🟡 中", 3: "🟢 低"}
        priority_str = priority_map.get(self.priority, "🟢 低")
        
        base = f"{self.id:3d}. [{status}] {self.title:<30} [{priority_str}]"
        
        if self.due_date:
            try:
                due = datetime.strptime(self.due_date, "%Y-%m-%d")
                today = datetime.now().date()
                days_left = (due.date() - today).days
                
                if days_left < 0:
                    due_str = f"❌ 逾期{-days_left}天"
                elif days_left == 0:
                    due_str = "⚠️ 今天截止"
                elif days_left <= 3:
                    due_str = f"⏰ {days_left}天后"
                else:
                    due_str = f"📅 {self.due_date}"
                base += f" {due_str}"
            except ValueError:
                base += f" 📅 {self.due_date}"
        
        if detailed:
            base += f"\n     📝 {self.description}" if self.description else ""
            base += f"\n     🕐 创建于: {self.created_at}"
            
        return base
    
    def is_overdue(self) -> bool:
        """检查任务是否逾期"""
        if not self.due_date or self.completed:
            return False
        
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
            return due < datetime.now().date()
        except ValueError:
            return False

class TodoManager:
    """待办事项管理器"""
    
    def __init__(self, data_file: str = "todos.json"):
        self.data_file = data_file
        self.todos: List[TodoItem] = []
        self.next_id = 1
        self.load_todos()
    
    def load_todos(self) -> None:
        """从JSON文件加载待办事项"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.todos = [TodoItem(**item) for item in data]
                    if self.todos:
                        self.next_id = max(todo.id for todo in self.todos) + 1
            except (json.JSONDecodeError, KeyError) as e:
                print(f"⚠️ 数据文件损坏，创建新的列表: {e}")
                self.todos = []
        else:
            self.todos = []
    
    def save_todos(self) -> None:
        """保存待办事项到JSON文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(todo) for todo in self.todos], 
                         f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"❌ 保存失败: {e}")
    
    def add_todo(self, title: str, description: str = "", 
                 priority: int = 3, due_date: str = None) -> TodoItem:
        """添加新待办事项"""
        if not title.strip():
            raise ValueError("任务标题不能为空")
        
        if priority not in [1, 2, 3]:
            priority = 3
        
        todo = TodoItem(
            id=self.next_id,
            title=title.strip(),
            description=description.strip(),
            priority=priority,
            due_date=due_date
        )
        
        self.todos.append(todo)
        self.next_id += 1
        self.save_todos()
        return todo
    
    def delete_todo(self, todo_id: int) -> bool:
        """删除指定ID的待办事项"""
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                self.todos.pop(i)
                self.save_todos()
                return True
        return False
    
    def complete_todo(self, todo_id: int) -> bool:
        """标记任务为完成/未完成"""
        for todo in self.todos:
            if todo.id == todo_id:
                todo.completed = not todo.completed
                self.save_todos()
                return True
        return False
    
    def update_todo(self, todo_id: int, **kwargs) -> bool:
        """更新任务信息"""
        for todo in self.todos:
            if todo.id == todo_id:
                for key, value in kwargs.items():
                    if hasattr(todo, key) and value is not None:
                        setattr(todo, key, value)
                self.save_todos()
                return True
        return False
    
    def list_todos(self, show_completed: bool = True, 
                   sort_by: str = "id") -> List[TodoItem]:
        """列出待办事项，支持排序"""
        todos = self.todos.copy()
        
        if not show_completed:
            todos = [todo for todo in todos if not todo.completed]
        
        # 排序逻辑
        if sort_by == "priority":
            todos.sort(key=lambda x: (x.priority, x.id))
        elif sort_by == "due_date":
            def get_due_date(todo):
                if todo.due_date:
                    try:
                        return datetime.strptime(todo.due_date, "%Y-%m-%d")
                    except ValueError:
                        return datetime.max
                return datetime.max
            todos.sort(key=lambda x: (get_due_date(x), x.priority))
        elif sort_by == "id":
            todos.sort(key=lambda x: x.id)
        
        return todos
    
    def search_todos(self, keyword: str) -> List[TodoItem]:
        """搜索任务标题和描述"""
        keyword = keyword.lower()
        return [todo for todo in self.todos 
                if keyword in todo.title.lower() or 
                keyword in todo.description.lower()]
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        total = len(self.todos)
        completed = sum(1 for todo in self.todos if todo.completed)
        overdue = sum(1 for todo in self.todos if todo.is_overdue())
        
        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "overdue": overdue,
            "completion_rate": (completed / total * 100) if total > 0 else 0
        }

def display_menu() -> None:
    """显示主菜单"""
    print("\n" + "="*50)
    print("📋 命令行待办事项管理器")
    print("="*50)
    print("1. 📝 添加新任务")
    print("2. 👁️  查看所有任务")
    print("3. 🔍 搜索任务")
    print("4. ✅ 标记完成/未完成")
    print("5. ✏️  编辑任务")
    print("6. 🗑️  删除任务")
    print("7. 📊 显示统计")
    print("8. 💾 导出任务")
    print("9. 📂 导入任务")
    print("0. 🚪 退出")
    print("-"*50)

def get_input(prompt: str, default: str = "") -> str:
    """获取用户输入，支持默认值"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()

def main():
    """主程序"""
    manager = TodoManager()
    
    # 如果有逾期任务，显示提醒
    overdue_todos = [todo for todo in manager.todos if todo.is_overdue()]
    if overdue_todos:
        print("\n⚠️  你有逾期任务：")
        for todo in overdue_todos[:3]:  # 只显示前3个
            print(f"   {todo.display()}")
        if len(overdue_todos) > 3:
            print(f"   ... 还有{len(overdue_todos)-3}个逾期任务")
    
    while True:
        display_menu()
        choice = get_input("请选择操作")
        
        try:
            if choice == "1":
                # 添加新任务
                print("\n📝 添加新任务")
                title = get_input("任务标题")
                if not title:
                    print("❌ 标题不能为空")
                    continue
                
                description = get_input("任务描述（可选）")
                priority_map = {"1": 1, "2": 2, "3": 3}
                priority_input = get_input("优先级 (1-高, 2-中, 3-低)", "3")
                priority = priority_map.get(priority_input, 3)
                
                due_date = get_input("截止日期 (YYYY-MM-DD，可选)")
                if due_date:
                    try:
                        datetime.strptime(due_date, "%Y-%m-%d")
                    except ValueError:
                        print("❌ 日期格式错误，应为 YYYY-MM-DD")
                        due_date = None
                
                todo = manager.add_todo(title, description, priority, due_date)
                print(f"✅ 已添加任务: {todo.title}")
                
            elif choice == "2":
                # 查看任务
                print("\n👁️  查看任务")
                print("1. 查看所有任务")
                print("2. 只查看未完成")
                print("3. 按优先级排序")
                print("4. 按截止日期排序")
                
                view_choice = get_input("请选择")
                show_completed = view_choice != "2"
                sort_by = "id"
                
                if view_choice == "3":
                    sort_by = "priority"
                elif view_choice == "4":
                    sort_by = "due_date"
                
                todos = manager.list_todos(show_completed, sort_by)
                
                if not todos:
                    print("📭 暂无任务")
                else:
                    print(f"\n📋 任务列表 (共{len(todos)}个):")
                    for todo in todos:
                        print(todo.display(detailed=True))
                        print()  # 空行分隔
                
            elif choice == "3":
                # 搜索任务
                keyword = get_input("🔍 搜索关键词")
                if keyword:
                    results = manager.search_todos(keyword)
                    if results:
                        print(f"找到 {len(results)} 个相关任务:")
                        for todo in results:
                            print(todo.display(detailed=True))
                            print()
                    else:
                        print("🔍 未找到相关任务")
                
            elif choice == "4":
                # 标记完成/未完成
                try:
                    todo_id = int(get_input("✅ 输入任务ID"))
                    if manager.complete_todo(todo_id):
                        print("✅ 状态已更新")
                    else:
                        print("❌ 未找到该任务")
                except ValueError:
                    print("❌ 请输入有效的任务ID")
                
            elif choice == "5":
                # 编辑任务
                try:
                    todo_id = int(get_input("✏️  输入要编辑的任务ID"))
                    
                    # 查找任务
                    target_todo = None
                    for todo in manager.todos:
                        if todo.id == todo_id:
                            target_todo = todo
                            break
                    
                    if not target_todo:
                        print("❌ 未找到该任务")
                        continue
                    
                    print(f"当前任务: {target_todo.display()}")
                    print("\n编辑选项:")
                    print("1. 修改标题")
                    print("2. 修改描述")
                    print("3. 修改优先级")
                    print("4. 修改截止日期")
                    
                    edit_choice = get_input("请选择")
                    
                    if edit_choice == "1":
                        new_title = get_input("新标题", target_todo.title)
                        if new_title:
                            manager.update_todo(todo_id, title=new_title)
                            print("✅ 标题已更新")
                    elif edit_choice == "2":
                        new_desc = get_input("新描述", target_todo.description)
                        manager.update_todo(todo_id, description=new_desc)
                        print("✅ 描述已更新")
                    elif edit_choice == "3":
                        new_priority = get_input("新优先级 (1-3)", str(target_todo.priority))
                        if new_priority in ["1", "2", "3"]:
                            manager.update_todo(todo_id, priority=int(new_priority))
                            print("✅ 优先级已更新")
                    elif edit_choice == "4":
                        new_due = get_input("新截止日期 (YYYY-MM-DD)", target_todo.due_date or "")
                        if new_due:
                            try:
                                datetime.strptime(new_due, "%Y-%m-%d")
                                manager.update_todo(todo_id, due_date=new_due)
                                print("✅ 截止日期已更新")
                            except ValueError:
                                print("❌ 日期格式错误")
                    else:
                        print("❌ 无效选择")
                        
                except ValueError:
                    print("❌ 请输入有效的任务ID")
                
            elif choice == "6":
                # 删除任务
                try:
                    todo_id = int(get_input("🗑️  输入要删除的任务ID"))
                    if manager.delete_todo(todo_id):
                        print("✅ 任务已删除")
                    else:
                        print("❌ 未找到该任务")
                except ValueError:
                    print("❌ 请输入有效的任务ID")
                
            elif choice == "7":
                # 显示统计
                stats = manager.get_stats()
                print(f"\n📊 任务统计:")
                print(f"   总计: {stats['total']} 个任务")
                print(f"   已完成: {stats['completed']} 个")
                print(f"   待完成: {stats['pending']} 个")
                print(f"   逾期: {stats['overdue']} 个")
                print(f"   完成率: {stats['completion_rate']:.1f}%")
                
                if stats['total'] > 0:
                    # 简单的进度条
                    bar_length = 20
                    completed_bar = int(stats['completion_rate'] / 100 * bar_length)
                    progress_bar = "[" + "█" * completed_bar + "░" * (bar_length - completed_bar) + "]"
                    print(f"   进度: {progress_bar} {stats['completion_rate']:.1f}%")
                
            elif choice == "8":
                # 导出任务
                export_file = get_input("💾 导出文件名", "todos_export.json")
                try:
                    with open(export_file, 'w', encoding='utf-8') as f:
                        json.dump([asdict(todo) for todo in manager.todos], 
                                 f, ensure_ascii=False, indent=2)
                    print(f"✅ 任务已导出到 {export_file}")
                except IOError as e:
                    print(f"❌ 导出失败: {e}")
                
            elif choice == "9":
                # 导入任务
                import_file = get_input("📂 导入文件名")
                if os.path.exists(import_file):
                    try:
                        with open(import_file, 'r', encoding='utf-8') as f:
                            imported_data = json.load(f)
                        
                        if isinstance(imported_data, list):
                            merge_choice = get_input("合并到现有任务？(y/n)", "y").lower()
                            if merge_choice == 'y':
                                # 合并导入
                                for item in imported_data:
                                    # 避免ID冲突
                                    item['id'] = manager.next_id
                                    manager.next_id += 1
                                    manager.todos.append(TodoItem(**item))
                            else:
                                # 替换现有
                                manager.todos = [TodoItem(**item) for item in imported_data]
                                if manager.todos:
                                    manager.next_id = max(todo.id for todo in manager.todos) + 1
                            
                            manager.save_todos()
                            print(f"✅ 已从 {import_file} 导入 {len(imported_data)} 个任务")
                        else:
                            print("❌ 导入文件格式错误")
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"❌ 导入文件解析错误: {e}")
                else:
                    print("❌ 文件不存在")
                
            elif choice == "0":
                # 退出
                print("\n👋 再见！")
                manager.save_todos()
                break
                
            else:
                print("❌ 无效选择，请重试")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  操作被中断")
        except Exception as e:
            print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()
