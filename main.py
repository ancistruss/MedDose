import ttkbootstrap as ttk
from tkinter import messagebox
from app import App
from db import init_db, add_default_data


def run_gui():

    #ініціалізація БД
    init_db()
    add_default_data()

    logic = App()

    #головне вікно
    win = ttk.Window(
        title="Медичний довідник",
        themename="darkly",
        size=(700, 520),
        resizable=(True, True)
    )

    header = ttk.Label(
        win,
        text="🧪 MedDose",
        font=("Segoe UI", 22, "bold"),
        bootstyle = "success"

    )
    header.pack(pady=10)

    subheader = ttk.Label(
        win,
        text="Пошук інформації та перевірка сумісності препаратів",
        font=("Segoe UI", 11)
    )
    subheader.pack()

    #notebook (вкладки)
    tabs = ttk.Notebook(win)
    tabs.pack(fill="both", expand=True, pady=10)

    #вкладка 1 - пошук
    tab_search = ttk.Frame(tabs)
    tabs.add(tab_search, text="Пошук ліків")

    ttk.Label(tab_search, text="Назва препарату:", font=("Segoe UI", 12)).pack(pady=5)
    search_entry = ttk.Entry(tab_search, width=40)
    search_entry.pack()

    search_output = ttk.Label(
        tab_search,
        text="",
        font=("Segoe UI", 11),
        justify="left",
        wraplength=600
    )
    search_output.pack(pady=10)

    def do_search():
        name = search_entry.get().strip()
        if not name:
            messagebox.showerror("Помилка", "Введіть назву!")
            return

        info = logic.get_info(name)
        if not info:
            search_output.config(text="❗ Препарат не знайдено", bootstyle="danger")
            return

        interactions = ", ".join(info["interactions"]) if info["interactions"] else "Немає"

        txt = (
            f"🔹 Назва: {info['name']}\n"
            f"🔹 Опис: {info['description']}\n"
            f"🔹 Несумісність: {interactions}"
        )

        search_output.config(text=txt, bootstyle="info")

    ttk.Button(tab_search, text="Пошук", bootstyle="primary", command=do_search).pack(pady=5)

    #вкладка 2 - сумісність
    tab_check = ttk.Frame(tabs)
    tabs.add(tab_check, text="Перевірка сумісності")

    ttk.Label(tab_check, text="Перший препарат:", font=("Segoe UI", 12)).pack(pady=5)
    med1 = ttk.Entry(tab_check, width=40)
    med1.pack()

    ttk.Label(tab_check, text="Другий препарат:", font=("Segoe UI", 12)).pack(pady=5)
    med2 = ttk.Entry(tab_check, width=40)
    med2.pack()

    result_label = ttk.Label(tab_check, text="", font=("Segoe UI", 14, "bold"))
    result_label.pack(pady=15)

    def check_compat():
        m1 = med1.get().strip()
        m2 = med2.get().strip()

        if not m1 or not m2:
            messagebox.showerror("Помилка", "Введіть обидві назви!")
            return

        ok, msg = logic.check_compatibility(m1, m2)

        if "не знайдено" in msg:
            messagebox.showerror("Помилка", msg)
            return

        if ok:
            result_label.config(text=f"{m1} + {m2} → СУМІСНІ", bootstyle="success")
        else:
            result_label.config(text=f"{m1} + {m2} → НЕСУМІСНІ", bootstyle="danger")

    ttk.Button(tab_check, text="Перевірити", bootstyle="primary", command=check_compat).pack(pady=10)


    #вкладка 3 - список ліків
    tab_list = ttk.Frame(tabs)
    tabs.add(tab_list, text="Список препаратів")

    ttk.Label(tab_list, text="Усі препарати з бази:", font=("Segoe UI", 12)).pack(pady=5)

    #таблиця
    table = ttk.Treeview(
        tab_list,
        columns=("name", "desc", "inter"),
        show="headings",
        height=15
    )

    table.heading("name", text="Назва")
    table.heading("desc", text="Опис")
    table.heading("inter", text="Несумісні")

    table.column("name", width=150)
    table.column("desc", width=280)
    table.column("inter", width=200)

    table.pack(fill="both", expand=True, padx=10, pady=10)

    #завантаження даних у таблицю
    def load_all():
        table.delete(*table.get_children())
        conn = logic.search("Aspirin")  #щоб ініціалізувати

        import sqlite3
        from db import get_connection

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, description, interactions FROM medicines")
        rows = cur.fetchall()
        conn.close()

        for r in rows:
            name, desc, inter = r
            table.insert("", "end", values=(name, desc, inter))

    load_all()

    win.mainloop()


if __name__ == "__main__":
    run_gui()
