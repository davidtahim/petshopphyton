import tkinter as tk
from tkinter import ttk


class PetShopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pet Shop")
        self.geometry("700x500")
        self.configure(bg="#f0f0f0")

        title = tk.Label(self, text="Sistema Pet Shop", font=("Arial", 18, "bold"), bg="#f0f0f0")
        title.pack(pady=20)

        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(frame, width=40).grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Telefone:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(frame, width=40).grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(frame, width=40).grid(row=2, column=1, pady=5, padx=10)

        ttk.Button(frame, text="Salvar cliente").grid(row=3, column=1, sticky="e", pady=15)

        self.mainloop()


if __name__ == "__main__":
    PetShopApp()
