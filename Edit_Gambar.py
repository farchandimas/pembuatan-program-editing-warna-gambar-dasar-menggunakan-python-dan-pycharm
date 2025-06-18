import cv2
import numpy as np
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

users = {}

class ModernImageEditor:
    def __init__(self, root):  # <-- Perbaikan di sini
        self.root = root
        self.root.title("✨ Modern Image Editor")
        self.root.geometry("900x700")
        self.root.configure(bg="#222831")

        self.original_image = None
        self.display_image = None

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", background="#222831", foreground="#eeeeee", font=('Segoe UI', 11))
        self.style.configure("TButton", background="#00adb5", foreground="#eeeeee", font=('Segoe UI', 10, 'bold'))
        self.style.map("TButton", background=[('active', '#007f8f')])

        self.show_login()

    def show_login(self):
        self.login_frame = Frame(self.root, bg="#222831")
        self.login_frame.pack(expand=True)

        ttk.Label(self.login_frame, text="Login to Modern Editor", font=('Segoe UI', 18, 'bold')).pack(pady=20)

        ttk.Label(self.login_frame, text="Username:").pack(anchor='w', padx=20)
        self.login_username = ttk.Entry(self.login_frame, font=('Segoe UI', 12))
        self.login_username.pack(padx=20, pady=5, fill='x')

        ttk.Label(self.login_frame, text="Password:").pack(anchor='w', padx=20)
        self.login_password = ttk.Entry(self.login_frame, show='*', font=('Segoe UI', 12))
        self.login_password.pack(padx=20, pady=5, fill='x')

        ttk.Button(self.login_frame, text="Login", command=self.login).pack(pady=15)
        ttk.Button(self.login_frame, text="Register", command=self.show_register).pack()

    def show_register(self):
        self.login_frame.pack_forget()
        self.register_frame = Frame(self.root, bg="#222831")
        self.register_frame.pack(expand=True)

        ttk.Label(self.register_frame, text="Register New Account", font=('Segoe UI', 18, 'bold')).pack(pady=20)

        ttk.Label(self.register_frame, text="Username:").pack(anchor='w', padx=20)
        self.reg_username = ttk.Entry(self.register_frame, font=('Segoe UI', 12))
        self.reg_username.pack(padx=20, pady=5, fill='x')

        ttk.Label(self.register_frame, text="Password:").pack(anchor='w', padx=20)
        self.reg_password = ttk.Entry(self.register_frame, show='*', font=('Segoe UI', 12))
        self.reg_password.pack(padx=20, pady=5, fill='x')

        ttk.Button(self.register_frame, text="Register", command=self.register).pack(pady=15)
        ttk.Button(self.register_frame, text="Back to Login", command=self.back_to_login).pack()

    def back_to_login(self):
        self.register_frame.pack_forget()
        self.show_login()

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        if username in users and users[username] == password:
            messagebox.showinfo("Login", "Login berhasil!")
            self.login_frame.pack_forget()
            self.show_editor()
        else:
            messagebox.showerror("Login", "Username atau password salah.")

    def register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        if username in users:
            messagebox.showwarning("Register", "Username sudah terdaftar.")
        else:
            users[username] = password
            messagebox.showinfo("Register", "Registrasi berhasil! Silakan login.")
            self.register_frame.pack_forget()
            self.show_login()

    def show_editor(self):
        self.editor_frame = Frame(self.root, bg="#222831")
        self.editor_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Left panel for image preview
        self.left_panel = Frame(self.editor_frame, bg="#393e46")
        self.left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))

        self.img_label = Label(self.left_panel, bg="#222831", relief="sunken", bd=2)
        self.img_label.pack(padx=20, pady=20, fill='both', expand=True)

        # Right panel for controls with scrollbar
        self.right_panel = Frame(self.editor_frame, bg="#393e46")
        self.right_panel.pack(side='right', fill='y', padx=(10, 0))

        canvas = Canvas(self.right_panel, bg="#393e46", highlightthickness=0, width=280)
        scrollbar = ttk.Scrollbar(self.right_panel, orient="vertical", command=canvas.yview)
        self.controls_frame = Frame(canvas, bg="#393e46")

        self.controls_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.controls_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons
        ttk.Button(self.controls_frame, text="Open Image 📁", command=self.load_image).pack(pady=10, fill='x')
        ttk.Button(self.controls_frame, text="Apply Filter 🎨", command=self.apply_filter).pack(pady=10, fill='x')
        ttk.Button(self.controls_frame, text="Save Image 💾", command=self.save_image).pack(pady=10, fill='x')
        ttk.Button(self.controls_frame, text="Exit 🚪", command=self.root.quit).pack(pady=20, fill='x')

        # Brightness slider
        ttk.Label(self.controls_frame, text="Brightness").pack(anchor='w', padx=10)
        self.brightness = ttk.Scale(self.controls_frame, from_=-100, to=100, command=self.update_image)
        self.brightness.set(0)
        self.brightness.pack(fill='x', padx=10, pady=5)

        # Contrast slider
        ttk.Label(self.controls_frame, text="Contrast").pack(anchor='w', padx=10)
        self.contrast = ttk.Scale(self.controls_frame, from_=-100, to=100, command=self.update_image)
        self.contrast.set(0)
        self.contrast.pack(fill='x', padx=10, pady=5)

        # Filter dropdown
        ttk.Label(self.controls_frame, text="Filter").pack(anchor='w', padx=10, pady=(10, 0))
        self.filter_var = StringVar()
        filter_menu = ttk.Combobox(self.controls_frame, textvariable=self.filter_var, state="readonly",
                                   values=["none", "cartoon", "sepia", "negative"])
        filter_menu.current(0)
        filter_menu.pack(fill='x', padx=10, pady=5)

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.original_image = cv2.imread(path)
            self.display_image = self.original_image.copy()
            self.brightness.set(0)
            self.contrast.set(0)
            self.filter_var.set("none")
            self.show_image()

    def show_image(self):
        if self.display_image is not None:
            h, w = self.display_image.shape[:2]
            max_w, max_h = 560, 560
            scale = min(max_w / w, max_h / h)
            resized = cv2.resize(self.display_image, (int(w * scale), int(h * scale)))
            img_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img_rgb)
            imgtk = ImageTk.PhotoImage(im_pil)
            self.img_label.imgtk = imgtk
            self.img_label.configure(image=imgtk)

    def update_image(self, event=None):
        if self.original_image is not None:
            brightness = self.brightness.get()
            contrast = self.contrast.get()
            alpha = contrast / 127 + 1.0
            beta = brightness
            edited = cv2.convertScaleAbs(self.original_image, alpha=alpha, beta=beta)
            self.display_image = edited
            self.show_image()

    def apply_filter(self):
        if self.original_image is not None:
            filter_name = self.filter_var.get()
            filtered_image = self.display_image.copy()

            if filter_name == "cartoon":
                gray = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
                gray = cv2.medianBlur(gray, 5)
                edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                              cv2.THRESH_BINARY, 9, 9)
                color = cv2.bilateralFilter(filtered_image, 9, 250, 250)
                filtered_image = cv2.bitwise_and(color, color, mask=edges)
            elif filter_name == "sepia":
                sepia_filter = np.array([[0.272, 0.534, 0.131],
                                         [0.349, 0.686, 0.168],
                                         [0.393, 0.769, 0.189]])
                filtered_image = cv2.transform(filtered_image, sepia_filter)
                filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)
            elif filter_name == "negative":
                filtered_image = cv2.bitwise_not(filtered_image)

            self.display_image = filtered_image
            self.show_image()

    def save_image(self):
        if self.display_image is not None:
            path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                filetypes=[("JPEG files", ".jpg"), ("PNG files", ".png")])
            if path:
                cv2.imwrite(path, self.display_image)
                messagebox.showinfo("Saved", f"Image saved to {path}")

# Main entry point - Perbaikan di sini
if __name__ == "__main__":
    root = Tk()
    app = ModernImageEditor(root)
    root.mainloop()
