import tkinter as tk
from tkinter import messagebox, ttk

from app.services.pet_service import PetShopService


class PetShopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Pet Shop")
        self.geometry("980x660")
        self.minsize(860, 520)
        self.configure(bg="#eef4ff")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Pet.TFrame", background="#eef4ff")
        style.configure("Header.TLabel", background="#eef4ff", foreground="#0f172a", font=("Arial", 22, "bold"))
        style.configure("Subtitle.TLabel", background="#eef4ff", foreground="#475569", font=("Arial", 11))
        style.configure("Section.TLabel", background="#eef4ff", foreground="#1f2937", font=("Arial", 10, "bold"))
        style.configure("Accent.TButton", font=("Arial", 10, "bold"))
        style.configure("Primary.TButton", font=("Arial", 11, "bold"), foreground="#ffffff")
        style.map(
            "Primary.TButton",
            background=[("active", "#2563eb"), ("pressed", "#1d4ed8")],
            foreground=[("active", "#ffffff"), ("pressed", "#ffffff")],
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#0f766e"), ("pressed", "#115e59")],
            foreground=[("active", "#ffffff"), ("pressed", "#ffffff")],
        )
        style.configure("Treeview", rowheight=26, fieldbackground="#ffffff", background="#ffffff", foreground="#1f2937")
        style.map("Treeview", background=[("selected", "#c7d2fe")], foreground=[("selected", "#111827")])

        self.service = PetShopService()

        self.landing_frame = ttk.Frame(self, padding=28, style="Pet.TFrame")
        self.landing_frame.pack(fill="both", expand=True)

        logo = ttk.Label(
            self.landing_frame,
            text="🐾 Pet Shop",
            style="Header.TLabel",
            justify="center",
        )
        logo.pack(pady=(30, 10))

        subtitle = ttk.Label(
            self.landing_frame,
            text="Gestão de clientes e animais",
            style="Subtitle.TLabel",
        )
        subtitle.pack(pady=(0, 25))

        self.menu_buttons = ttk.Frame(self.landing_frame, style="Pet.TFrame")
        self.menu_buttons.pack(pady=12)

        btn_clientes = ttk.Button(
            self.menu_buttons,
            text="Clientes",
            command=lambda: self.open_section("clientes"),
            style="Primary.TButton",
            width=22,
        )
        btn_clientes.grid(row=0, column=0, padx=12, pady=10)

        btn_animais = ttk.Button(
            self.menu_buttons,
            text="Animais",
            command=lambda: self.open_section("animais"),
            style="Accent.TButton",
            width=22,
        )
        btn_animais.grid(row=0, column=1, padx=12, pady=10)

        btn_sair = ttk.Button(
            self.menu_buttons,
            text="Sair",
            command=self.destroy,
            width=22,
        )
        btn_sair.grid(row=1, column=0, columnspan=2, padx=12, pady=(8, 10), sticky="ew")

        self.content = ttk.Frame(self, style="Pet.TFrame")
        self.content.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(self.content)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        self.cliente_tab = ttk.Frame(self.notebook, padding=12, style="Pet.TFrame")
        self.animal_tab = ttk.Frame(self.notebook, padding=12, style="Pet.TFrame")
        self.notebook.add(self.cliente_tab, text="Clientes")
        self.notebook.add(self.animal_tab, text="Animais")

        self.status_var = tk.StringVar(value="Carregando registros...")
        status = ttk.Label(
            self.content,
            textvariable=self.status_var,
            style="Section.TLabel",
            padding=(18, 0, 18, 12),
        )
        status.pack(fill="x")

        self._build_cliente_tab()
        self._build_animal_tab()
        self.refresh_all()

        self.notebook.pack_forget()
        self.content.pack_forget()

    def open_section(self, section_name):
        self.landing_frame.pack_forget()
        self.content.pack(fill="both", expand=True)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        if section_name == "clientes":
            self.notebook.select(self.cliente_tab)
        else:
            self.notebook.select(self.animal_tab)

    def _build_cliente_tab(self):
        content = ttk.Frame(self.cliente_tab, style="Pet.TFrame")
        content.pack(fill="both", expand=True)

        form = ttk.Frame(content, padding=(8, 8, 8, 6), style="Pet.TFrame")
        form.pack(fill="x")

        fields = [
            ("ID", 0),
            ("Nome", 1),
            ("Telefone", 2),
            ("Email", 3),
        ]

        self.cliente_entries = {}
        for label, row in fields:
            lbl = ttk.Label(form, text=f"{label}:", style="Section.TLabel")
            lbl.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=6)
            entry = ttk.Entry(form, width=48)
            entry.grid(row=row, column=1, sticky="ew", pady=6)
            self.cliente_entries[label] = entry

        form.columnconfigure(1, weight=1)

        buttons = [
            ("Salvar", self.salvar_cliente),
            ("Buscar", self.buscar_cliente),
            ("Atualizar", self.atualizar_cliente),
            ("Excluir", self.excluir_cliente),
            ("Listar", self.listar_clientes),
        ]

        buttons_frame = ttk.Frame(content, padding=(8, 2, 8, 8), style="Pet.TFrame")
        buttons_frame.pack(fill="x")
        for idx, (text, command) in enumerate(buttons):
            btn = ttk.Button(buttons_frame, text=text, command=command, style="Accent.TButton")
            btn.grid(row=0, column=idx, padx=(0, 8), pady=6, sticky="ew")
        for i in range(len(buttons)):
            buttons_frame.columnconfigure(i, weight=1)

        self.clientes_tree = ttk.Treeview(
            content,
            columns=("id", "nome", "telefone", "email"),
            show="headings",
            height=12,
        )
        self.clientes_tree.heading("id", text="ID")
        self.clientes_tree.heading("nome", text="Nome")
        self.clientes_tree.heading("telefone", text="Telefone")
        self.clientes_tree.heading("email", text="Email")
        self.clientes_tree.column("id", width=70, anchor="center")
        self.clientes_tree.column("nome", width=220)
        self.clientes_tree.column("telefone", width=160)
        self.clientes_tree.column("email", width=290)
        self.clientes_tree.bind("<<TreeviewSelect>>", self.on_select_cliente)
        self.clientes_tree.pack(fill="both", expand=True, padx=8, pady=(0, 6))

    def _build_animal_tab(self):
        content = ttk.Frame(self.animal_tab, style="Pet.TFrame")
        content.pack(fill="both", expand=True)

        form = ttk.Frame(content, padding=(8, 8, 8, 6), style="Pet.TFrame")
        form.pack(fill="x")

        fields = [
            ("ID", 0),
            ("Nome", 1),
            ("Espécie", 2),
            ("Raça", 3),
            ("Idade", 4),
            ("Dono ID", 5),
        ]

        self.animal_entries = {}
        for label, row in fields:
            lbl = ttk.Label(form, text=f"{label}:", style="Section.TLabel")
            lbl.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=6)
            entry = ttk.Entry(form, width=48)
            entry.grid(row=row, column=1, sticky="ew", pady=6)
            self.animal_entries[label] = entry

        form.columnconfigure(1, weight=1)

        buttons = [
            ("Salvar", self.salvar_animal),
            ("Buscar", self.buscar_animal),
            ("Atualizar", self.atualizar_animal),
            ("Excluir", self.excluir_animal),
            ("Listar", self.listar_animais),
        ]

        buttons_frame = ttk.Frame(content, padding=(8, 2, 8, 8), style="Pet.TFrame")
        buttons_frame.pack(fill="x")
        for idx, (text, command) in enumerate(buttons):
            btn = ttk.Button(buttons_frame, text=text, command=command, style="Accent.TButton")
            btn.grid(row=0, column=idx, padx=(0, 8), pady=6, sticky="ew")
        for i in range(len(buttons)):
            buttons_frame.columnconfigure(i, weight=1)

        self.animais_tree = ttk.Treeview(
            content,
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
        self.animais_tree.column("id", width=70, anchor="center")
        self.animais_tree.column("nome", width=150)
        self.animais_tree.column("especie", width=130)
        self.animais_tree.column("raca", width=140)
        self.animais_tree.column("idade", width=90, anchor="center")
        self.animais_tree.column("dono_id", width=100, anchor="center")
        self.animais_tree.bind("<<TreeviewSelect>>", self.on_select_animal)
        self.animais_tree.pack(fill="both", expand=True, padx=8, pady=(0, 6))

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
            self.refresh_all()
            self.reset_cliente_fields()
        except ValueError as exc:
            messagebox.showerror("Erro", str(exc))

    def buscar_cliente(self):
        cliente_id = self.cliente_entries["ID"].get().strip()
        if not cliente_id:
            self.listar_clientes()
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
            self.refresh_all()
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
            self.refresh_all()
            self.reset_cliente_fields()

    def listar_clientes(self):
        clientes = self.service.listar_clientes()
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)

        for cliente in clientes:
            self.clientes_tree.insert(
                "",
                tk.END,
                values=(cliente.id, cliente.nome, cliente.telefone, cliente.email),
            )

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
            self.refresh_all()
            self.reset_animal_fields()
        except ValueError as exc:
            messagebox.showerror("Erro", str(exc))

    def buscar_animal(self):
        animal_id = self.animal_entries["ID"].get().strip()
        if not animal_id:
            self.listar_animais()
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
            self.refresh_all()
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
            self.refresh_all()
            self.reset_animal_fields()

    def listar_animais(self):
        animais = self.service.listar_animais()
        for item in self.animais_tree.get_children():
            self.animais_tree.delete(item)

        for animal in animais:
            self.animais_tree.insert(
                "",
                tk.END,
                values=(animal.id, animal.nome, animal.especie, animal.raca, animal.idade, animal.dono_id),
            )

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

    def refresh_all(self):
        self.listar_clientes()
        self.listar_animais()
        clientes = self.service.listar_clientes()
        animais = self.service.listar_animais()
        self.status_var.set(f"Clientes: {len(clientes)} | Animais: {len(animais)}")


if __name__ == "__main__":
    PetShopApp().mainloop()
