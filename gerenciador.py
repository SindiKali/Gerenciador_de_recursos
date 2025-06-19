import tkinter as tk
from tkinter import messagebox, ttk
import json

class GerenciadorRecursos:
    def __init__(self, root):
        self.root = root
        self.recursos = []
        self.modo_escuro = False
        
        # Configurações padrão
        self.resolucoes = {
            '800x600': (800, 600),
            '1024x768': (1024, 768),
            '1280x1024': (1280, 1024),
            '1920x1080': (1920, 1080)
        }
        
        # Variável para armazenar o item do menu de modo escuro
        self.modo_escuro_menu_item = None
        
        # Configurar interface primeiro
        self.configurar_interface()
        
        # Depois criar menu
        self.criar_menu()
        
        # Por último aplicar tema
        self.aplicar_tema()
        
        # Definir resolução inicial
        self.alterar_resolucao(self.resolucoes['1024x768'])

    def criar_menu(self):
        menubar = tk.Menu(self.root)
        
        # Menu de Configurações
        config_menu = tk.Menu(menubar, tearoff=0)
        
        # Submenu de Resolução
        resolucao_menu = tk.Menu(config_menu, tearoff=0)
        for texto, resolucao in self.resolucoes.items():
            resolucao_menu.add_command(
                label=texto, 
                command=lambda r=resolucao: self.alterar_resolucao(r)
            )
        
        config_menu.add_cascade(label="Resolução", menu=resolucao_menu)
        
        # Adicionar item do modo escuro
        self.modo_escuro_menu_item = tk.BooleanVar(value=self.modo_escuro)
        config_menu.add_checkbutton(
            label="Modo Escuro", 
            variable=self.modo_escuro_menu_item,
            command=self.alternar_modo_escuro
        )
        
        config_menu.add_separator()
        config_menu.add_command(label="Sair", command=self.root.quit)
        
        menubar.add_cascade(label="Configurações", menu=config_menu)
        
        self.root.config(menu=menubar)

    def configurar_interface(self):
        # Frame principal para melhor organização
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.label_recurso = ttk.Label(
            self.main_frame, 
            text="Recurso:"
        )
        self.label_recurso.pack(pady=5)
        
        self.entrada_recurso = ttk.Entry(self.main_frame)
        self.entrada_recurso.pack(fill=tk.X, pady=5)
        
        # Frame para os botões
        botoes_frame = ttk.Frame(self.main_frame)
        botoes_frame.pack(fill=tk.X, pady=5)
        
        self.botao_adicionar = ttk.Button(
            botoes_frame, 
            text="Adicionar", 
            command=self.adicionar_recurso
        )
        self.botao_adicionar.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.botao_remover = ttk.Button(
            botoes_frame, 
            text="Remover", 
            command=self.remover_recurso
        )
        self.botao_remover.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.lista_recursos = tk.Listbox(
            self.main_frame,
            bg='white',
            fg='black'
        )
        self.lista_recursos.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.carregar_recursos()

    def alternar_modo_escuro(self):
        self.modo_escuro = not self.modo_escuro
        self.aplicar_tema()

    def aplicar_tema(self):
        if self.modo_escuro:
            # Cores do modo escuro
            bg_color = '#2d2d2d'
            fg_color = '#ffffff'
            entry_bg = '#3d3d3d'
            listbox_bg = '#3d3d3d'
            listbox_fg = '#ffffff'
            button_bg = '#4a4a4a'
            button_fg = '#000000'  # Fonte preta mesmo no modo escuro
            button_active_bg = '#5a5a5a'
        else:
            # Cores do modo claro
            bg_color = '#f0f0f0'
            fg_color = '#000000'
            entry_bg = '#ffffff'
            listbox_bg = '#ffffff'
            listbox_fg = '#000000'
            button_bg = '#e0e0e0'
            button_fg = '#000000'  # Fonte preta
            button_active_bg = '#d0d0d0'
        
        # Aplicar cores aos widgets
        style = ttk.Style()
        
        # Configurar estilo para os botões ttk (mantendo fonte preta)
        style.configure('TButton',
                      background=button_bg,
                      foreground=button_fg,  # Sempre preto
                      bordercolor=bg_color)
        
        style.map('TButton',
                background=[('active', button_active_bg)],
                foreground=[('active', button_fg)])  # Sempre preto
        
        # Configurar outros estilos
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TEntry', 
                      fieldbackground=entry_bg, 
                      foreground=fg_color,
                      insertcolor=fg_color)
        
        # Aplicar estilos
        self.main_frame.configure(style='TFrame')
        self.label_recurso.configure(style='TLabel')
        self.entrada_recurso.configure(style='TEntry')
        self.botao_adicionar.configure(style='TButton')
        self.botao_remover.configure(style='TButton')
        
        # Configurar Listbox (não é ttk, precisa ser configurado separadamente)
        self.lista_recursos.config(
            bg=listbox_bg,
            fg=listbox_fg,
            selectbackground='#4a6987',
            selectforeground='#ffffff'
        )

    def alterar_resolucao(self, resolucao):
        largura, altura = resolucao
        self.root.geometry(f"{largura}x{altura}")

    def adicionar_recurso(self):
        recurso = self.entrada_recurso.get()
        if recurso:
            self.recursos.append(recurso)
            self.atualizar_lista()
            self.entrada_recurso.delete(0, tk.END)
            self.salvar_recursos()
        else:
            messagebox.showwarning(
                "Aviso", 
                "Por favor, insira um recurso."
            )

    def remover_recurso(self):
        selecionado = self.lista_recursos.curselection()
        if selecionado:
            self.recursos.pop(selecionado[0])
            self.atualizar_lista()
            self.salvar_recursos()
        else:
            messagebox.showwarning(
                "Aviso", 
                "Por favor, selecione um recurso para remover."
            )

    def atualizar_lista(self):
        self.lista_recursos.delete(0, tk.END)
        for recurso in self.recursos:
            self.lista_recursos.insert(tk.END, recurso)

    def salvar_recursos(self):
        with open('recursos.json', 'w') as arquivo:
            json.dump(self.recursos, arquivo)

    def carregar_recursos(self):
        try:
            with open('recursos.json', 'r') as arquivo:
                self.recursos = json.load(arquivo)
                self.atualizar_lista()
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = GerenciadorRecursos(root)
    root.mainloop()
