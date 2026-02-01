import os
import json
import bcrypt
from tkinter import *
from tkinter import messagebox


# ---------------- Variables ----------------
INACTIVITY_TIMEOUT = 15000  # 15 seconds (milliseconds)
inactivity_timer = None


DATA_FILE = "vault.json"





# ------------------ FUNCTIONS ------------------

def create_master_password(password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with open("master.hash", "wb") as f:
        f.write(hashed)

def verify_master_password(password):
    with open("master.hash", "rb") as f:
        stored_hash = f.read()
    return bcrypt.checkpw(password.encode(), stored_hash)

def reset_inactivity_timer(event=None):
    global inactivity_timer

    if inactivity_timer:
        root.after_cancel(inactivity_timer)

    inactivity_timer = root.after(INACTIVITY_TIMEOUT, auto_close_app)

def login_with_enter(event):
    login()



def auto_close_app():
    warning = Toplevel(root)
    warning.overrideredirect(True)
    warning.configure(bg="#7f1d1d")

    warning.geometry("320x60+" +
                     str(root.winfo_x() + 50) + "+" +
                     str(root.winfo_y() + 120))

    Label(
        warning,
        text="⏳ Session expired due to inactivity",
        bg="#7f1d1d",
        fg="white",
        font=("Segoe UI", 10, "bold")
    ).pack(expand=True)

    warning.after(2000, lambda: root.destroy())


def show_welcome_and_open_dashboard():
    popup = Toplevel(root)
    popup.overrideredirect(True)
    popup.configure(bg="#111827")

    popup_width = 320
    popup_height = 90

    root.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - (popup_width // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (popup_height // 2)

    popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    Label(
        popup,
        text="✅ Access Granted\nWelcome to Password Manager!",
        bg="#111827",
        fg="#38bdf8",
        font=("Segoe UI", 11, "bold"),
        justify="center"
    ).pack(expand=True)

    def transition():
        popup.destroy()
        root.destroy()      # 🔥 DESTROY LOGIN COMPLETELY
        open_app()          # Open dashboard as new app

    popup.after(2000, transition)


def login():
    password = password_entry.get()

    if password == "":
        messagebox.showwarning("Warning", "Password cannot be empty!")
        return

    if not os.path.exists("master.hash"):
        create_master_password(password)
        messagebox.showinfo("Success", "Master password created!\nLogin again.")
        password_entry.delete(0, END)
    else:
        if verify_master_password(password):
            reset_inactivity_timer()  # reset before leaving login
            show_welcome_and_open_dashboard()

        else:
            messagebox.showerror("Access Denied", "Incorrect Master Password!")

# ------------------ UI SETUP ------------------

root = Tk()

# -------- ACTIVITY TRACKING --------
root.bind_all("<Key>", reset_inactivity_timer)
root.bind_all("<Motion>", reset_inactivity_timer)
root.bind_all("<Button>", reset_inactivity_timer)


root.title("Password Manager Login")
root.geometry("1000x600")
root.resizable(True, True)
root.configure(bg="#1f2933")  # Dark background

# ------------------ CARD FRAME ------------------

card = Frame(root, bg="#111827", width=320, height=220)
card.place(relx=0.5, rely=0.5, anchor=CENTER)

# ------------------ HEADING ------------------

Label(
    card,
    text="🔐 Secure Login",
    bg="#111827",
    fg="#38bdf8",
    font=("Segoe UI", 16, "bold")
).pack(pady=15)

Label(
    card,
    text="Enter Master Password",
    bg="#111827",
    fg="#e5e7eb",
    font=("Segoe UI", 10)
).pack(pady=5)

# ------------------ PASSWORD ENTRY ------------------

password_entry = Entry(
    card,
    show="*",
    font=("Segoe UI", 12),
    width=22,
    relief=FLAT,
    bg="#1f2933",
    fg="white",
    insertbackground="white",
    highlightthickness=2,
    highlightbackground="#38bdf8",
    highlightcolor="#38bdf8"
)
password_entry.pack(pady=10)
password_entry.bind("<Return>", login_with_enter)



# ------------------ LOGIN BUTTON ------------------

Button(
    card,
    text="Login",
    command=login,
    bg="#38bdf8",
    fg="#000000",
    font=("Segoe UI", 11, "bold"),
    relief=FLAT,
    width=15,
    cursor="hand2"
).pack(pady=15)

# ------------------ FOOTER ------------------

Label(
    root,
    text="Password Manager • Python + Security",
    bg="#1f2933",
    fg="#9ca3af",
    font=("Segoe UI", 9)
).pack(side=BOTTOM, pady=8)



def open_app():
    app = Tk()
    app.title("Password Manager")
    app.geometry("1000x600")
    app.configure(bg="#0f172a")
    app.resizable(True, True)

    # ----------- HEADER -----------
    Label(app, text="🔑 Password Manager",
          bg="#0f172a", fg="#38bdf8",
          font=("Segoe UI", 18, "bold")).pack(pady=15)
    

    # ----------- TOP BAR (SEARCH + ACTIONS) -----------

    top_bar = Frame(app, bg="#0f172a")
    top_bar.pack(fill="x", padx=30, pady=(5, 10))

    # ----------- MAIN CONTENT AREA -----------
    main_container = Frame(app, bg="#0f172a")
    main_container.pack(fill="both", expand=True)

    dashboard_frame = Frame(main_container, bg="#0f172a")
    dashboard_frame.pack(fill="both", expand=True)

    # ---------- SCROLLABLE CARDS AREA ----------

    cards_canvas = Canvas(
        dashboard_frame,
        bg="#0f172a",
        highlightthickness=0
    )
    cards_canvas.pack(side=LEFT, fill="both", expand=True)

    scrollbar = Scrollbar(
        dashboard_frame,
        orient=VERTICAL,
        command=cards_canvas.yview
    )
    scrollbar.pack(side=RIGHT, fill="y")

    cards_canvas.configure(yscrollcommand=scrollbar.set)

    cards_container = Frame(cards_canvas, bg="#0f172a")

    cards_canvas.create_window(
        (0, 0),
        window=cards_container,
        anchor="nw"
    )

    def update_scroll_region(event=None):
        cards_canvas.configure(scrollregion=cards_canvas.bbox("all"))

    cards_container.bind("<Configure>", update_scroll_region)



    add_frame = Frame(main_container, bg="#0f172a")


    # 🔍 Search Entry
    search_entry = Entry(
        top_bar,
        font=("Segoe UI", 11),
        bg="#020617",
        fg="#e5e7eb",
        insertbackground="white",
        relief=FLAT
    )
    

    search_entry.insert(0, "Search passwords...")
    search_entry.pack(side=LEFT, fill="x", expand=True, ipady=8)

    


    saved_passwords = []


    def show_add_section():
        dashboard_frame.pack_forget()

        # 🔥 FORCE GEOMETRY UPDATE
        app.update_idletasks()

        add_frame.pack(fill="both", expand=True)




    # ☰ Actions Button
    actions_btn = Button(
            top_bar,
            text="☰ Actions",
            bg="#38bdf8",
            fg="black",
            font=("Segoe UI", 10, "bold"),
            relief=FLAT,
            cursor="hand2"
        )
    actions_btn.pack(side=RIGHT, padx=(10, 0))

    actions_menu = Menu(app, tearoff=0, bg="#020617", fg="white")
    actions_menu.add_command(
            label="➕ Add Password",
            command=show_add_section
        )

    def open_actions_menu(event):
        actions_menu.tk_popup(event.x_root, event.y_root)

    actions_btn.bind("<Button-1>", open_actions_menu)



    # Placeholder behavior
    def clear_placeholder(event):
        if search_entry.get() == "Search passwords...":
            search_entry.delete(0, END)

    def add_placeholder(event):
        if search_entry.get() == "":
            search_entry.insert(0, "Search passwords...")

    search_entry.bind("<FocusIn>", clear_placeholder)
    search_entry.bind("<FocusOut>", add_placeholder)



    def load_passwords():
        if not os.path.exists(DATA_FILE):
            return

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            saved_passwords.clear()
            saved_passwords.extend(data)


    def show_dashboard():
        add_frame.pack_forget()
        dashboard_frame.pack(fill="both", expand=True)
        refresh_cards()


    load_passwords()

    # 🔥 delay dashboard rendering until window is ready
    app.after(100, show_dashboard)




    def create_rounded_card(parent, site, user, pwd):

        is_visible = False
        masked_pwd = "•" * len(pwd)


        record = {
                "site": site,
                "user": user,
                "password": pwd
            }


        parent.update_idletasks()
        w = max(parent.winfo_width() - 160, 700)
        h = 90
        r = 20

        canvas = Canvas(
            parent,
            width=w,
            height=h,
            bg="#0f172a",
            highlightthickness=0
        )
        canvas.pack(padx=80, pady=10)

        canvas.create_polygon(
            r, 0,
            w - r, 0,
            w, r,
            w, h - r,
            w - r, h,
            r, h,
            0, h - r,
            0, r,
            fill="#020617",
            smooth=True
        )

        canvas.create_text(
            25, 28,
            anchor="w",
            text=f"🌐 {site}",
            fill="white",
            font=("Segoe UI", 12, "bold")
        )

        canvas.create_text(
            25, 58,
            anchor="w",
            text=f"👤 {user}",
            fill="#cbd5f5",
            font=("Segoe UI", 10)
        )
        password_text = canvas.create_text(
            25, 78,
            anchor="w",
            text=f"🔑 {masked_pwd}",
            fill="#94a3b8",
            font=("Segoe UI", 10)
        )

        def toggle_password():
            nonlocal is_visible
            if is_visible:
                canvas.itemconfig(password_text, text=f"🔑 {masked_pwd}")
                eye_btn.config(text="👁")
            else:
                canvas.itemconfig(password_text, text=f"🔑 {pwd}")
                eye_btn.config(text="🙈")
            is_visible = not is_visible




        # COPY BUTTON
        Button(
            canvas,
            text="📋 Copy",
            bg="#38bdf8",
            fg="black",
            font=("Segoe UI", 9, "bold"),
            relief=FLAT,
            cursor="hand2",
            command=lambda: copy_password(pwd)
        ).place(x=w-190, y=30, width=80, height=30)

        # DELETE BUTTON (🔥 OPTION 3)
        Button(
            canvas,
            text="🗑",
            bg="#ef4444",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief=FLAT,
            cursor="hand2",
            command=lambda: animate_delete(canvas, record)
        ).place(x=w-95, y=30, width=45, height=30)

        eye_btn = Button(
            canvas,
            text="👁",
            bg="#64748b",
            fg="black",
            font=("Segoe UI", 9, "bold"),
            relief=FLAT,
            cursor="hand2",
            command=toggle_password
        )
        eye_btn.place(x=w-290, y=30, width=80, height=30)




    def copy_password(pwd):
                app.clipboard_clear()
                app.clipboard_append(pwd)
                show_toast("🔐 Password copied")



    def show_toast(message):
        toast = Toplevel(app)
        toast.overrideredirect(True)
        toast.configure(bg="#020617")

        toast.geometry(f"220x40+{app.winfo_x()+380}+{app.winfo_y()+520}")

        Label(
            toast,
            text=message,
            bg="#020617",
            fg="#38bdf8",
            font=("Segoe UI", 10, "bold")
        ).pack(expand=True)
        toast.after(1500, toast.destroy)


    def animate_delete(canvas, record):
        canvas.destroy()

        if record in saved_passwords:
            saved_passwords.remove(record)
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(saved_passwords, f, indent=4)

        refresh_cards()


    def refresh_cards():
        for widget in cards_container.winfo_children():
            widget.destroy()

        if not saved_passwords:
            Label(
                cards_container,
                text="No passwords saved yet",
                bg="#0f172a",
                fg="#9ca3af",
                font=("Segoe UI", 11)
            ).pack(pady=20)
            return

        for item in saved_passwords:
            create_rounded_card(
                cards_container,
                item["site"],
                item.get("user", ""),
                item["password"]
            )


    def filter_cards(event=None):
        query = search_entry.get().lower().strip()

        for widget in cards_container.winfo_children():
            widget.destroy()

        if query == "" or query == "search passwords...":
            refresh_cards()
            return

        matched = [
            item for item in saved_passwords
            if query in item["site"].lower()
            or query in item.get("user", "").lower()
        ]

        if not matched:
            Label(
                cards_container,
                text="No matching passwords found",
                bg="#0f172a",
                fg="#9ca3af",
                font=("Segoe UI", 11)
            ).pack(pady=20)
            return

        for item in matched:
            create_rounded_card(
                cards_container,
                item["site"],
                item.get("user", ""),
                item["password"]
            )

    search_entry.bind("<KeyRelease>", filter_cards)




    def save_password():
        site = site_entry.get().strip()
        user = user_entry.get().strip()
        pwd = pass_entry.get().strip()

        if site == "" or pwd == "":
            messagebox.showwarning("Warning", "Website and Password are required")
            return

        saved_passwords.append({
            "site": site,
            "user": user,
            "password": pwd
        })

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(saved_passwords, f, indent=4)

        site_entry.delete(0, END)
        user_entry.delete(0, END)
        pass_entry.delete(0, END)

        show_dashboard()   # 🔥 refresh immediately



    Label(
        add_frame,
        text="➕ Add New Password",
        bg="#0f172a",
        fg="#38bdf8",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=20)

    def create_input(label_text):
        Label(add_frame, text=label_text,
            bg="#0f172a", fg="#e5e7eb").pack(anchor="w", padx=250)

        entry = Entry(
            add_frame,
            font=("Segoe UI", 11),
            bg="#020617",
            fg="white",
            insertbackground="white",
            relief=FLAT
        )
        entry.pack(fill="x", padx=250, ipady=6, pady=(0, 15))
        return entry

    site_entry = create_input("Website")
    user_entry = create_input("Username / Email")
    pass_entry = create_input("Password")

    Button(
        add_frame,
        text="💾 Save Password",
        bg="#22c55e",
        fg="black",
        font=("Segoe UI", 11, "bold"),
        relief=FLAT,
        height=2,
        command=save_password
    ).pack(pady=10)

    Button(
        add_frame,
        text="⬅ Back to Dashboard",
        bg="#1f2933",
        fg="white",
        font=("Segoe UI", 10),
        relief=FLAT,
        command=show_dashboard
    ).pack()


    def _on_mousewheel(event):
        cards_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    cards_canvas.bind_all("<MouseWheel>", _on_mousewheel)



    app.mainloop()


reset_inactivity_timer()


root.mainloop()