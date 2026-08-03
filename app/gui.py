import tkinter as tk
from tkinter import messagebox, ttk

from app.services.pet_service import PetShopService


class PetShopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Pet Shop")
        self.geometry("900x600")
        self.minsize(800, 500)
        self.configure(bg="#f3f3f3")

        self.service = PetShopService()

        title = tk.Label(
            self,
            text="Pet Shop - Gestão de Clientes e Animais",
            font=("Arial", 18, "bold"),
            bg="#f3f3f3",
            pady=15,
        )
        title.pack()

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.cliente_tab = ttk.Frame(notebook, padding=10)
        self.animal_tab = ttk.Frame(notebook, padding=10)
        notebook.add(self.cliente_tab, text="Clientes")
        notebook.add(self.animal_tab, text="Animais")

        self._build_cliente_tab()
        self._build_animal_tab()

        self.refresh_all()

    def _build_cliente_tab(self):
        frame = ttk.Frame(self.cliente_tab)
        frame.pack(fill="x", pady=(0, 10))

        fields = [
            ("ID", 0),
            ("Nome", 1),
            ("Telefone", 2),
            ("Email", 3),
        ]

        self.cliente_entries = {}
        for label, row in fields:
            lbl = ttk.Label(frame, text=f"{label}:")
            lbl.grid(row=row, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
            self.cliente_entries[label] = entry

        buttons = [
            ("Salvar", self.salvar_cliente),
            ("Buscar", self.buscar_cliente),
            ("Atualizar", self.atualizar_cliente),
            ("Excluir", self.excluir_cliente),
            ("Listar", self.listar_clientes),
        ]

        for idx, (text, command) in enumerate(buttons):
            btn = ttk.Button(frame, text=text, command=command)
            btn.grid(row=4, column=idx, padx=5, pady=10, sticky="ew")

        self.clientes_tree = ttk.Treeview(
            self.cliente_tab,
            columns=("id", "nome", "telefone", "email"),
            show="headings",
        )
        self.clientes_tree.heading("id", text="ID")
        self.clientes_tree.heading("nome", text="Nome")
        self.clientes_tree.heading("telefone", text="Telefone")
        self.clientes_tree.heading("email", text="Email")
        self.clientes_tree.column("id", width=60, anchor="center")
        self.clientes_tree.column("nome", width=180)
        self.clientes_tree.column("telefone", width=150)
        self.clientes_tree.column("email", width=220)
        self.clientes_tree.bind("<<TreeviewSelect>>", self.on_select_cliente)
        self.clientes_tree.pack(fill="both", expand=True)

    def _build_animal_tab(self):
        frame = ttk.Frame(self.animal_tab)
        frame.pack(fill="x", pady=(0, 10))

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
            lbl = ttk.Label(frame, text=f"{label}:")
            lbl.grid(row=row, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
            self.animal_entries[label] = entry

        buttons = [
            ("Salvar", self.salvar_animal),
            ("Buscar", self.buscar_animal),
            ("Atualizar", self.atualizar_animal),
            ("Excluir", self.excluir_animal),
            ("Listar", self.listar_animais),
        ]

        for idx, (text, command) in enumerate(buttons):
            btn = ttk.Button(frame, text=text, command=command)
            btn.grid(row=6, column=idx, padx=5, pady=10, sticky="ew")

        self.animais_tree = ttk.Treeview(
            self.animal_tab,
            columns=("id", "nome", "especie", "raca", "idade", "dono_id"),
            show="headings",
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
        self.animais_tree.column("raca", width=140)
        self.animais_tree.column("idade", width=80, anchor="center")
        self.animais_tree.column("dono_id", width=80, anchor="center")
        self.animais_tree.bind("<<TreeviewSelect>>", self.on_select_animal)
        self.animais_tree.pack(fill="both", expand=True)

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


if __name__ == "__main__":
    PetShopApp().mainloop()
