import tkinter as tk
from tkinter import messagebox, ttk

from app.services.pet_service import PetShopService


class PetShopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pet Shop")
        self.geometry("900x600")
        self.minsize(760, 500)
        self.configure(bg="#f4f7fb")

        self.service = PetShopService()

        self.home = tk.Frame(self, bg="#f4f7fb", padx=30, pady=30)
        self.home.pack(fill="both", expand=True)

        title = tk.Label(
            self.home,
            text="🐾 Pet Shop",
            font=("Arial", 26, "bold"),
            bg="#f4f7fb",
            fg="#1f2937",
        )
        title.pack(pady=(20, 10))

        subtitle = tk.Label(
            self.home,
            text="Sistema simples de gestão",
            font=("Arial", 12),
            bg="#f4f7fb",
            fg="#475569",
        )
        subtitle.pack(pady=(0, 30))

        button_frame = tk.Frame(self.home, bg="#f4f7fb")
        button_frame.pack()

        tk.Button(
            button_frame,
            text="Clientes",
            width=20,
            height=2,
            bg="#2563eb",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.show_clientes,
        ).grid(row=0, column=0, padx=12, pady=12)

        tk.Button(
            button_frame,
            text="Animais",
            width=20,
            height=2,
            bg="#0f766e",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.show_animais,
        ).grid(row=0, column=1, padx=12, pady=12)

        tk.Button(
            button_frame,
            text="Sair",
            width=42,
            height=2,
            bg="#e2e8f0",
            fg="#111827",
            font=("Arial", 10, "bold"),
            command=self.destroy,
        ).grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=(8, 0))

        self.clientes_page = tk.Frame(self, bg="#f4f7fb", padx=18, pady=18)
        self.animais_page = tk.Frame(self, bg="#f4f7fb", padx=18, pady=18)

        self._build_clientes_page()
        self._build_animais_page()

        self.home.pack(fill="both", expand=True)
        self.clientes_page.pack_forget()
        self.animais_page.pack_forget()

    def _build_clientes_page(self):
        title = tk.Label(
            self.clientes_page,
            text="Clientes",
            font=("Arial", 20, "bold"),
            bg="#f4f7fb",
            fg="#111827",
        )
        title.pack(anchor="w", pady=(8, 12))

        form = tk.Frame(self.clientes_page, bg="#f4f7fb")
        form.pack(fill="x", pady=(0, 10))

        self.cliente_entries = {}
        labels = ["ID", "Nome", "Telefone", "Email"]
        for idx, label in enumerate(labels):
            tk.Label(form, text=f"{label}:", bg="#f4f7fb", font=("Arial", 10, "bold")).grid(row=idx, column=0, sticky="w", padx=(0, 8), pady=6)
            entry = tk.Entry(form, width=35, font=("Arial", 10))
            entry.grid(row=idx, column=1, sticky="ew", padx=(0, 10), pady=6)
            self.cliente_entries[label] = entry
        form.columnconfigure(1, weight=1)

        actions = tk.Frame(self.clientes_page, bg="#f4f7fb")
        actions.pack(fill="x", pady=(0, 10))
        commands = [
            ("Salvar", self.salvar_cliente),
            ("Buscar", self.buscar_cliente),
            ("Atualizar", self.atualizar_cliente),
            ("Excluir", self.excluir_cliente),
            ("Voltar", self.show_home),
        ]
        for idx, (text, command) in enumerate(commands):
            cor = "#2563eb" if text != "Voltar" else "#94a3b8"
            tk.Button(actions, text=text, width=12, bg=cor, fg="white", font=("Arial", 10, "bold"), command=command).grid(row=0, column=idx, padx=6)

        self.clientes_tree = ttk.Treeview(
            self.clientes_page,
            columns=("id", "nome", "telefone", "email"),
            show="headings",
            height=12,
        )
        self.clientes_tree.heading("id", text="ID")
        self.clientes_tree.heading("nome", text="Nome")
        self.clientes_tree.heading("telefone", text="Telefone")
        self.clientes_tree.heading("email", text="Email")
        self.clientes_tree.column("id", width=60, anchor="center")
        self.clientes_tree.column("nome", width=180)
        self.clientes_tree.column("telefone", width=140)
        self.clientes_tree.column("email", width=220)
        self.clientes_tree.bind("<<TreeviewSelect>>", self.on_select_cliente)
        self.clientes_tree.pack(fill="both", expand=True)

    def _build_animais_page(self):
        title = tk.Label(
            self.animais_page,
            text="Animais",
            font=("Arial", 20, "bold"),
            bg="#f4f7fb",
            fg="#111827",
        )
        title.pack(anchor="w", pady=(8, 12))

        form = tk.Frame(self.animais_page, bg="#f4f7fb")
        form.pack(fill="x", pady=(0, 10))

        self.animal_entries = {}
        labels = ["ID", "Nome", "Espécie", "Raça", "Idade", "Dono ID"]
        for idx, label in enumerate(labels):
            tk.Label(form, text=f"{label}:", bg="#f4f7fb", font=("Arial", 10, "bold")).grid(row=idx, column=0, sticky="w", padx=(0, 8), pady=6)
            entry = tk.Entry(form, width=35, font=("Arial", 10))
            entry.grid(row=idx, column=1, sticky="ew", padx=(0, 10), pady=6)
            self.animal_entries[label] = entry
        form.columnconfigure(1, weight=1)

        actions = tk.Frame(self.animais_page, bg="#f4f7fb")
        actions.pack(fill="x", pady=(0, 10))
        commands = [
            ("Salvar", self.salvar_animal),
            ("Buscar", self.buscar_animal),
            ("Atualizar", self.atualizar_animal),
            ("Excluir", self.excluir_animal),
            ("Voltar", self.show_home),
        ]
        for idx, (text, command) in enumerate(commands):
            cor = "#0f766e" if text != "Voltar" else "#94a3b8"
            tk.Button(actions, text=text, width=12, bg=cor, fg="white", font=("Arial", 10, "bold"), command=command).grid(row=0, column=idx, padx=6)

        self.animais_tree = ttk.Treeview(
            self.animais_page,
            columns=("id", "nome", "especie", "raca", "idade", "dono_id"),
            show="headings",
            height=12,
        )
        self.animais_tree.heading("id", text="ID")
        self.animais_tree.heading("nome", text="Nome")
        self.animais_tree.heading("especie", text="Espécie")
        self.animais_tree.heading("raca", text="Raça")
        self.animais_tree.heading("idade", text="Idade")
        self.animais_tree.heading("dono_id", text="Dono ID")
        self.animais_tree.column("id", width=60, anchor="center")
        self.animais_tree.column("nome", width=140)
        self.animais_tree.column("especie", width=120)
        self.animais_tree.column("raca", width=130)
        self.animais_tree.column("idade", width=80, anchor="center")
        self.animais_tree.column("dono_id", width=90, anchor="center")
        self.animais_tree.bind("<<TreeviewSelect>>", self.on_select_animal)
        self.animais_tree.pack(fill="both", expand=True)

    def show_home(self):
        self.home.pack(fill="both", expand=True)
        self.clientes_page.pack_forget()
        self.animais_page.pack_forget()

    def show_clientes(self):
        self.home.pack_forget()
        self.clientes_page.pack(fill="both", expand=True)
        self.animais_page.pack_forget()
        self.refresh_clientes()

    def show_animais(self):
        self.home.pack_forget()
        self.animais_page.pack(fill="both", expand=True)
        self.clientes_page.pack_forget()
        self.refresh_animais()

    def reset_cliente_fields(self):
        for key in self.cliente_entries:
            self.cliente_entries[key].delete(0, tk.END)

    def reset_animal_fields(self):
        for key in self.animal_entries:
            self.animal_entries[key].delete(0, tk.END)

    def _get_cliente_form(self):
        return {
            "id": self.cliente_entries["ID"].get().strip(),
            "nome": self.cliente_entries["Nome"].get().strip(),
            "telefone": self.cliente_entries["Telefone"].get().strip(),
            "email": self.cliente_entries["Email"].get().strip(),
        }

    def _get_animal_form(self):
        return {
            "id": self.animal_entries["ID"].get().strip(),
            "nome": self.animal_entries["Nome"].get().strip(),
            "especie": self.animal_entries["Espécie"].get().strip(),
            "raca": self.animal_entries["Raça"].get().strip(),
            "idade": self.animal_entries["Idade"].get().strip(),
            "dono_id": self.animal_entries["Dono ID"].get().strip(),
        }

    def salvar_cliente(self):
        dados = self._get_cliente_form()
        try:
            cliente = self.service.cadastrar_cliente(dados["nome"], dados["telefone"], dados["email"])
            messagebox.showinfo("Sucesso", f"Cliente cadastrado com ID {cliente['id']}")
            self.refresh_clientes()
            self.reset_cliente_fields()
        except ValueError as exc:
            messagebox.showerror("Erro", str(exc))

    def buscar_cliente(self):
        cliente_id = self.cliente_entries["ID"].get().strip()
        if not cliente_id:
            self.refresh_clientes()
            return
        cliente = self.service.buscar_cliente(int(cliente_id))
        if cliente is None:
            messagebox.showinfo("Busca", "Cliente não encontrado.")
            return
        self.reset_cliente_fields()
        self.cliente_entries["ID"].insert(0, str(cliente.id))
        self.cliente_entries["Nome"].insert(0, cliente.nome)
        self.cliente_entries["Telefone"].insert(0, cliente.telefone)
        self.cliente_entries["Email"].insert(0, cliente.email)

    def atualizar_cliente(self):
        dados = self._get_cliente_form()
        if not dados["id"]:
            messagebox.showerror("Erro", "Informe o ID do cliente para atualizar.")
            return
        try:
            cliente = self.service.atualizar_cliente(int(dados["id"]), dados["nome"], dados["telefone"], dados["email"])
            messagebox.showinfo("Sucesso", f"Cliente atualizado: {cliente['nome']}")
            self.refresh_clientes()
            self.reset_cliente_fields()
        except ValueError as exc:
            messagebox.showerror("Erro", str(exc))

    def excluir_cliente(self):
        cliente_id = self.cliente_entries["ID"].get().strip()
        if not cliente_id:
            messagebox.showerror("Erro", "Informe o ID do cliente para excluir.")
            return
        ok = messagebox.askyesno("Confirmação", f"Deseja excluir o cliente ID {cliente_id}?")
        if ok:
            self.service.excluir_cliente(int(cliente_id))
            messagebox.showinfo("Sucesso", "Cliente excluído.")
            self.refresh_clientes()
            self.reset_cliente_fields()

    def refresh_clientes(self):
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        for cliente in self.service.listar_clientes():
            self.clientes_tree.insert("", tk.END, values=(cliente.id, cliente.nome, cliente.telefone, cliente.email))

    def on_select_cliente(self, event):
        item = self.clientes_tree.selection()
        if not item:
            return
        values = self.clientes_tree.item(item[0], "values")
        self.reset_cliente_fields()
        self.cliente_entries["ID"].insert(0, str(values[0]))
        self.cliente_entries["Nome"].insert(0, values[1])
        self.cliente_entries["Telefone"].insert(0, values[2])
        self.cliente_entries["Email"].insert(0, values[3])

    def salvar_animal(self):
        dados = self._get_animal_form()
        try:
            animal = self.service.cadastrar_animal(
                dados["nome"],
                dados["especie"],
                dados["raca"],
                int(dados["idade"]),
                int(dados["dono_id"]),
            )
            messagebox.showinfo("Sucesso", f"Animal cadastrado com ID {animal['id']}")
            self.refresh_animais()
            self.reset_animal_fields()
        except ValueError as exc:
            messagebox.showerror("Erro", str(exc))

    def buscar_animal(self):
        animal_id = self.animal_entries["ID"].get().strip()
        if not animal_id:
            self.refresh_animais()
            return
        animal = self.service.buscar_animal(int(animal_id))
        if animal is None:
            messagebox.showinfo("Busca", "Animal não encontrado.")
            return
        self.reset_animal_fields()
        self.animal_entries["ID"].insert(0, str(animal.id))
        self.animal_entries["Nome"].insert(0, animal.nome)
        self.animal_entries["Espécie"].insert(0, animal.especie)
        self.animal_entries["Raça"].insert(0, animal.raca)
        self.animal_entries["Idade"].insert(0, str(animal.idade))
        self.animal_entries["Dono ID"].insert(0, str(animal.dono_id))

    def atualizar_animal(self):
        dados = self._get_animal_form()
        if not dados["id"]:
            messagebox.showerror("Erro", "Informe o ID do animal para atualizar.")
            return
        try:
            animal = self.service.atualizar_animal(
                int(dados["id"]),
                dados["nome"],
                dados["especie"],
                dados["raca"],
                int(dados["idade"]),
                int(dados["dono_id"]),
            )
            messagebox.showinfo("Sucesso", f"Animal atualizado: {animal['nome']}")
            self.refresh_animais()
            self.reset_animal_fields()
        except ValueError as exc:
            messagebox.showerror("Erro", str(exc))

    def excluir_animal(self):
        animal_id = self.animal_entries["ID"].get().strip()
        if not animal_id:
            messagebox.showerror("Erro", "Informe o ID do animal para excluir.")
            return
        ok = messagebox.askyesno("Confirmação", f"Deseja excluir o animal ID {animal_id}?")
        if ok:
            self.service.excluir_animal(int(animal_id))
            messagebox.showinfo("Sucesso", "Animal excluído.")
            self.refresh_animais()
            self.reset_animal_fields()

    def refresh_animais(self):
        for item in self.animais_tree.get_children():
            self.animais_tree.delete(item)
        for animal in self.service.listar_animais():
            self.animais_tree.insert("", tk.END, values=(animal.id, animal.nome, animal.especie, animal.raca, animal.idade, animal.dono_id))

    def on_select_animal(self, event):
        item = self.animais_tree.selection()
        if not item:
            return
        values = self.animais_tree.item(item[0], "values")
        self.reset_animal_fields()
        self.animal_entries["ID"].insert(0, str(values[0]))
        self.animal_entries["Nome"].insert(0, values[1])
        self.animal_entries["Espécie"].insert(0, values[2])
        self.animal_entries["Raça"].insert(0, values[3])
        self.animal_entries["Idade"].insert(0, str(values[4]))
        self.animal_entries["Dono ID"].insert(0, str(values[5]))


if __name__ == "__main__":
    app = PetShopApp()
    app.mainloop()
