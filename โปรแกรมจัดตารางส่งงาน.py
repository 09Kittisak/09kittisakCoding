import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import os

# ============================================================
# TaskMate - โปรแกรมจัดการงาน/เตือนการบ้าน
# สร้างด้วย Python + Tkinter
# ============================================================

DATA_FILE = "taskmate_data.json"

BLUE = "#1769E8"
TEXT = "#17191C"
MUTED = "#69707D"
BG = "#F5F7FB"
WHITE = "#FFFFFF"
GREEN = "#35B968"
RED = "#F05454"
ORANGE = "#F5A623"


class TaskMate:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskMate - จัดการงานค้าง")
        self.root.geometry("950x850")
        self.root.minsize(760, 700)
        self.root.configure(bg=BG)

        self.tasks = self.load_tasks()
        self.current_filter = "all"

        self.setup_style()
        self.build_ui()
        self.refresh()

    # -------------------- Data --------------------

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        return [
            {
                "id": 1,
                "name": "ส่งรายงานการตลาด",
                "date": today,
                "time": "11:59",
                "priority": "สูง",
                "done": False
            },
            {
                "id": 2,
                "name": "ประชุมทีมโปรเจกต์",
                "date": today,
                "time": "14:00",
                "priority": "ปานกลาง",
                "done": False
            },
            {
                "id": 3,
                "name": "ออกกำลังกาย 30 นาที",
                "date": today,
                "time": "19:00",
                "priority": "ต่ำ",
                "done": False
            },
            {
                "id": 4,
                "name": "จ่ายค่าน้ำ-ค่าไฟ",
                "date": tomorrow,
                "time": "09:00",
                "priority": "ปานกลาง",
                "done": False
            }
        ]

    def save_tasks(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    # -------------------- UI --------------------

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "TButton",
            font=("Tahoma", 11),
            padding=8
        )

        style.configure(
            "TCombobox",
            font=("Tahoma", 11)
        )

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=WHITE, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        menu_btn = tk.Button(
            header,
            text="☰",
            font=("Arial", 25),
            bg=WHITE,
            fg=TEXT,
            bd=0,
            command=self.show_menu,
            cursor="hand2"
        )
        menu_btn.pack(side="left", padx=28)

        notify_btn = tk.Button(
            header,
            text="🔔  3",
            font=("Tahoma", 13),
            bg=WHITE,
            fg=TEXT,
            bd=0,
            command=self.show_notifications,
            cursor="hand2"
        )
        notify_btn.pack(side="right", padx=28)

        # Main scrollable area
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            outer,
            bg=BG,
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            outer,
            orient="vertical",
            command=canvas.yview
        )
        self.content = tk.Frame(canvas, bg=BG)

        self.content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw"
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas = canvas

        # Hero
        hero = tk.Frame(self.content, bg=BG)
        hero.pack(fill="x", padx=42, pady=(25, 15))

        text_box = tk.Frame(hero, bg=BG)
        text_box.pack(side="left")

        tk.Label(
            text_box,
            text="สวัสดีตอนเช้า! ☀️",
            font=("Tahoma", 28, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(anchor="w")

        tk.Label(
            text_box,
            text="อย่าลืม จัดการงานค้างของคุณนะ 😊",
            font=("Tahoma", 16),
            fg=TEXT,
            bg=BG
        ).pack(anchor="w", pady=(7, 0))

        tk.Label(
            hero,
            text="📋\n⏰",
            font=("Segoe UI Emoji", 42),
            fg=BLUE,
            bg=BG,
            justify="center"
        ).pack(side="right", padx=25)

        # Statistics
        self.stats_frame = tk.Frame(self.content, bg=BG)
        self.stats_frame.pack(fill="x", padx=42, pady=10)

        for i in range(4):
            self.stats_frame.grid_columnconfigure(i, weight=1)

        self.stat_labels = {}

        self.create_stat_card(
            0, "📋", "ทั้งหมด", "total", "#EAF2FF", "#B9D2FF"
        )
        self.create_stat_card(
            1, "🕐", "ค้างอยู่", "pending", "#FFF8E9", "#FFE0A0"
        )
        self.create_stat_card(
            2, "🚩", "วันนี้", "today", "#FFF0F0", "#FFD0D0"
        )
        self.create_stat_card(
            3, "✓", "เสร็จแล้ว", "done", "#EDFFF2", "#C6EBCF"
        )

        # Today section
        self.today_section = tk.Frame(self.content, bg=BG)
        self.today_section.pack(fill="x", padx=42, pady=(20, 10))

        today_header = tk.Frame(self.today_section, bg=BG)
        today_header.pack(fill="x")

        tk.Label(
            today_header,
            text="งานที่ต้องทำวันนี้",
            font=("Tahoma", 21, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(side="left")

        tk.Button(
            today_header,
            text="ดูทั้งหมด  ›",
            font=("Tahoma", 12, "bold"),
            bg=BG,
            fg=BLUE,
            bd=0,
            command=self.filter_today,
            cursor="hand2"
        ).pack(side="right")

        self.today_list = tk.Frame(self.today_section, bg=BG)
        self.today_list.pack(fill="x", pady=10)

        # Upcoming section
        self.upcoming_section = tk.Frame(self.content, bg=BG)
        self.upcoming_section.pack(fill="x", padx=42, pady=(8, 100))

        upcoming_header = tk.Frame(self.upcoming_section, bg=BG)
        upcoming_header.pack(fill="x")

        tk.Label(
            upcoming_header,
            text="งานที่ใกล้ถึงกำหนด",
            font=("Tahoma", 21, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(side="left")

        tk.Button(
            upcoming_header,
            text="ดูทั้งหมด  ›",
            font=("Tahoma", 12, "bold"),
            bg=BG,
            fg=BLUE,
            bd=0,
            command=self.filter_upcoming,
            cursor="hand2"
        ).pack(side="right")

        self.upcoming_list = tk.Frame(self.upcoming_section, bg=BG)
        self.upcoming_list.pack(fill="x", pady=10)

        # Floating add button
        add_button = tk.Button(
            self.root,
            text="+",
            font=("Arial", 32),
            bg=BLUE,
            fg=WHITE,
            activebackground="#0E57C8",
            activeforeground=WHITE,
            bd=0,
            relief="flat",
            width=3,
            height=1,
            command=self.add_task_window,
            cursor="hand2"
        )
        add_button.place(relx=0.90, rely=0.82, anchor="center")

        # Bottom navigation
        nav = tk.Frame(self.root, bg=WHITE, height=75)
        nav.pack(side="bottom", fill="x")
        nav.pack_propagate(False)

        nav_items = [
            ("⌂", "หน้าหลัก"),
            ("☷", "งานของฉัน"),
            ("▣", "ปฏิทิน"),
            ("◇", "หมวดหมู่"),
            ("♙", "ฉัน")
        ]

        for icon, label in nav_items:
            b = tk.Button(
                nav,
                text=f"{icon}\n{label}",
                font=("Tahoma", 10),
                bg=WHITE,
                fg=BLUE if label == "หน้าหลัก" else MUTED,
                bd=0,
                cursor="hand2",
                command=lambda x=label: self.navigation(x)
            )
            b.pack(side="left", expand=True, fill="both")

    def create_stat_card(self, column, icon, title, key, bg, border):
        card = tk.Frame(
            self.stats_frame,
            bg=bg,
            highlightbackground=border,
            highlightthickness=1
        )
        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=6,
            ipady=12
        )

        tk.Label(
            card,
            text=f"{icon}  {title}",
            font=("Tahoma", 13),
            bg=bg,
            fg=TEXT
        ).pack()

        number = tk.Label(
            card,
            text="0",
            font=("Arial", 32, "bold"),
            bg=bg,
            fg=TEXT
        )
        number.pack(pady=(5, 0))

        tk.Label(
            card,
            text="งาน",
            font=("Tahoma", 12),
            bg=bg,
            fg=TEXT
        ).pack()

        self.stat_labels[key] = number

    # -------------------- Refresh --------------------

    def refresh(self):
        today = datetime.now().strftime("%Y-%m-%d")

        total = len(self.tasks)
        pending = len([t for t in self.tasks if not t["done"]])
        today_count = len([t for t in self.tasks if t["date"] == today])
        done = len([t for t in self.tasks if t["done"]])

        self.stat_labels["total"].config(text=str(total))
        self.stat_labels["pending"].config(text=str(pending))
        self.stat_labels["today"].config(text=str(today_count))
        self.stat_labels["done"].config(text=str(done))

        self.render_lists()

    def render_lists(self):
        for widget in self.today_list.winfo_children():
            widget.destroy()

        for widget in self.upcoming_list.winfo_children():
            widget.destroy()

        today = datetime.now().strftime("%Y-%m-%d")

        today_tasks = [
            t for t in self.tasks
            if t["date"] == today
        ]

        upcoming_tasks = [
            t for t in self.tasks
            if t["date"] > today
        ]

        upcoming_tasks.sort(
            key=lambda t: (t["date"], t["time"])
        )

        if self.current_filter == "today":
            upcoming_tasks = []
        elif self.current_filter == "upcoming":
            today_tasks = []

        if today_tasks:
            for task in today_tasks:
                self.create_task_card(
                    self.today_list,
                    task
                )
        else:
            tk.Label(
                self.today_list,
                text="ไม่มีงานในรายการนี้ 🎉",
                font=("Tahoma", 13),
                bg=BG,
                fg=MUTED
            ).pack(anchor="w", pady=15)

        if upcoming_tasks:
            for task in upcoming_tasks[:5]:
                self.create_task_card(
                    self.upcoming_list,
                    task,
                    upcoming=True
                )
        else:
            tk.Label(
                self.upcoming_list,
                text="ไม่มีงานใกล้ถึงกำหนด",
                font=("Tahoma", 13),
                bg=BG,
                fg=MUTED
            ).pack(anchor="w", pady=15)

    def create_task_card(self, parent, task, upcoming=False):
        priority = task["priority"]

        if priority == "สูง":
            accent = RED
            badge_bg = "#FFE5E5"
            badge_fg = "#D92D35"
        elif priority == "ปานกลาง":
            accent = ORANGE
            badge_bg = "#FFF0D9"
            badge_fg = "#D97706"
        else:
            accent = GREEN
            badge_bg = "#E0F8E8"
            badge_fg = "#159447"

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground="#E7EBF0",
            highlightthickness=1
        )
        card.pack(fill="x", pady=6)

        # Colored left border
        border = tk.Frame(card, bg=accent, width=5)
        border.pack(side="left", fill="y")

        inner = tk.Frame(card, bg=WHITE)
        inner.pack(fill="both", expand=True, padx=14, pady=13)

        check_text = "✓" if task["done"] else ""

        check = tk.Button(
            inner,
            text=check_text,
            font=("Arial", 16, "bold"),
            width=2,
            height=1,
            bg="#E8EBF0" if not task["done"] else GREEN,
            fg=WHITE,
            bd=0,
            relief="flat",
            command=lambda tid=task["id"]: self.toggle_task(tid),
            cursor="hand2"
        )
        check.pack(side="left", padx=(0, 13))

        info = tk.Frame(inner, bg=WHITE)
        info.pack(side="left", fill="both", expand=True)

        name_font = ("Tahoma", 16)
        if task["done"]:
            name_font = ("Tahoma", 16, "overstrike")

        tk.Label(
            info,
            text=task["name"],
            font=name_font,
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        date_text = self.format_date(task["date"])

        tk.Label(
            info,
            text=f"▣  {date_text} {task['time']}",
            font=("Tahoma", 11),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(4, 0))

        badge = tk.Label(
            inner,
            text=priority,
            font=("Tahoma", 10, "bold"),
            bg=badge_bg,
            fg=badge_fg,
            padx=10,
            pady=5
        )
        badge.pack(side="right", padx=8)

        delete = tk.Button(
            inner,
            text="☆",
            font=("Arial", 22),
            bg=WHITE,
            fg="#9AA1AD",
            bd=0,
            command=lambda tid=task["id"]: self.delete_task(tid),
            cursor="hand2"
        )
        delete.pack(side="right")

    # -------------------- Actions --------------------

    def format_date(self, date_string):
        today = datetime.now().date()
        d = datetime.strptime(date_string, "%Y-%m-%d").date()

        if d == today:
            return "วันนี้"
        if d == today + timedelta(days=1):
            return "พรุ่งนี้"

        return d.strftime("%d/%m/%Y")

    def toggle_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["done"] = not task["done"]
                break

        self.save_tasks()
        self.refresh()

    def delete_task(self, task_id):
        answer = messagebox.askyesno(
            "ลบงาน",
            "คุณต้องการลบงานนี้หรือไม่?"
        )

        if answer:
            self.tasks = [
                t for t in self.tasks
                if t["id"] != task_id
            ]
            self.save_tasks()
            self.refresh()

    def add_task_window(self):
        win = tk.Toplevel(self.root)
        win.title("เพิ่มงานใหม่")
        win.geometry("450x500")
        win.configure(bg=WHITE)
        win.resizable(False, False)

        tk.Label(
            win,
            text="เพิ่มงานใหม่",
            font=("Tahoma", 22, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w", padx=30, pady=(25, 15))

        form = tk.Frame(win, bg=WHITE)
        form.pack(fill="both", expand=True, padx=30)

        tk.Label(
            form,
            text="ชื่องาน",
            font=("Tahoma", 11),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w")

        name_entry = tk.Entry(
            form,
            font=("Tahoma", 13),
            relief="solid",
            bd=1
        )
        name_entry.pack(fill="x", ipady=7, pady=(5, 15))

        tk.Label(
            form,
            text="วันที่ (YYYY-MM-DD)",
            font=("Tahoma", 11),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w")

        date_entry = tk.Entry(
            form,
            font=("Tahoma", 13),
            relief="solid",
            bd=1
        )
        date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )
        date_entry.pack(fill="x", ipady=7, pady=(5, 15))

        tk.Label(
            form,
            text="เวลา",
            font=("Tahoma", 11),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w")

        time_entry = tk.Entry(
            form,
            font=("Tahoma", 13),
            relief="solid",
            bd=1
        )
        time_entry.insert(0, "12:00")
        time_entry.pack(fill="x", ipady=7, pady=(5, 15))

        tk.Label(
            form,
            text="ความสำคัญ",
            font=("Tahoma", 11),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w")

        priority = ttk.Combobox(
            form,
            values=["สูง", "ปานกลาง", "ต่ำ"],
            state="readonly",
            font=("Tahoma", 12)
        )
        priority.set("ปานกลาง")
        priority.pack(fill="x", ipady=5, pady=(5, 15))

        buttons = tk.Frame(form, bg=WHITE)
        buttons.pack(fill="x", pady=10)

        tk.Button(
            buttons,
            text="ยกเลิก",
            font=("Tahoma", 11),
            bg="#EEF1F5",
            bd=0,
            padx=20,
            pady=8,
            command=win.destroy
        ).pack(side="right", padx=5)

        def save_new_task():
            name = name_entry.get().strip()
            date = date_entry.get().strip()
            time = time_entry.get().strip()

            if not name:
                messagebox.showwarning(
                    "ข้อมูลไม่ครบ",
                    "กรุณาใส่ชื่องาน"
                )
                return

            try:
                datetime.strptime(date, "%Y-%m-%d")
                datetime.strptime(time, "%H:%M")
            except ValueError:
                messagebox.showwarning(
                    "รูปแบบไม่ถูกต้อง",
                    "กรุณาใส่วันที่เป็น YYYY-MM-DD และเวลาเป็น HH:MM"
                )
                return

            new_task = {
                "id": int(datetime.now().timestamp() * 1000),
                "name": name,
                "date": date,
                "time": time,
                "priority": priority.get(),
                "done": False
            }

            self.tasks.append(new_task)
            self.save_tasks()
            self.refresh()
            win.destroy()

        tk.Button(
            buttons,
            text="เพิ่มงาน",
            font=("Tahoma", 11, "bold"),
            bg=BLUE,
            fg=WHITE,
            bd=0,
            padx=20,
            pady=8,
            command=save_new_task
        ).pack(side="right")

        name_entry.focus()

    def filter_today(self):
        if self.current_filter == "today":
            self.current_filter = "all"
        else:
            self.current_filter = "today"
        self.refresh()

    def filter_upcoming(self):
        if self.current_filter == "upcoming":
            self.current_filter = "all"
        else:
            self.current_filter = "upcoming"
        self.refresh()

    def navigation(self, name):
        if name == "หน้าหลัก":
            self.current_filter = "all"
            self.refresh()
        elif name == "งานของฉัน":
            self.current_filter = "all"
            messagebox.showinfo(
                "งานของฉัน",
                f"มีงานทั้งหมด {len(self.tasks)} งาน"
            )
        elif name == "ปฏิทิน":
            messagebox.showinfo(
                "ปฏิทิน",
                "ส่วนปฏิทินสามารถพัฒนาต่อได้ในเวอร์ชันถัดไป"
            )
        elif name == "หมวดหมู่":
            messagebox.showinfo(
                "หมวดหมู่",
                "สามารถเพิ่มระบบหมวดหมู่ เช่น การบ้าน / งานกลุ่ม / ส่วนตัว"
            )
        elif name == "ฉัน":
            messagebox.showinfo(
                "ฉัน",
                "TaskMate\nโปรแกรมจัดการงานและการบ้าน"
            )

    def show_menu(self):
        messagebox.showinfo(
            "เมนู",
            "TaskMate\n\n"
            "• เพิ่มงาน\n"
            "• จัดการงาน\n"
            "• ดูงานที่ใกล้ถึงกำหนด\n"
            "• บันทึกข้อมูลอัตโนมัติ"
        )

    def show_notifications(self):
        today = datetime.now().strftime("%Y-%m-%d")
        today_tasks = [
            t for t in self.tasks
            if t["date"] == today and not t["done"]
        ]

        if not today_tasks:
            messagebox.showinfo(
                "การแจ้งเตือน",
                "ไม่มีการแจ้งเตือน 🎉"
            )
            return

        text = "🔔 งานที่ต้องทำวันนี้\n\n"
        for task in today_tasks:
            text += f"• {task['name']} เวลา {task['time']}\n"

        messagebox.showinfo(
            "การแจ้งเตือน",
            text
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskMate(root)
    root.mainloop()
