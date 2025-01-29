import tkinter as tk
from tkinter import messagebox
import json
from localizacao import traduzir

class GerenciadorRecursos:
    def __init__(self, root, idioma='pt'):
        self.root = root
        self.idioma = idioma
        self.recursos = []

        self.root.title(traduzir(self.idioma, 'titulo'))

        self.label_recurso = tk.Label(root, text=traduzir(self.idioma, 'recurso'))
        self.label_recurso.pack()

        self.entrada_recurso = tk.Entry(root)
        self.entrada_recurso.pack()

        self.botao_adicionar = tk.Button(root, text=traduzir(self.idioma, 'adicionar'), command=self.adicionar_recurso)
        self.botao_adicionar.pack()

        self.botao_remover = tk.Button(root, text=traduzir(self.idioma, 'remover'), command=self.remover_recurso)
        self.botao_remover.pack()

        self.lista_recursos = tk.Listbox(root)
        self.lista_recursos.pack()

        self.carregar_recursos()

    def adicionar_recurso(self):
        recurso = self.entrada_recurso.get()
        if recurso:
            self.recursos.append(recurso)
            self.atualizar_lista()
            self.entrada_recurso.delete(0, tk.END)
            self.salvar_recursos()
        else:
            messagebox.showwarning(traduzir(self.idioma, 'titulo'), 'Por favor, insira um recurso.')

    def remover_recurso(self):
        selecionado = self.lista_recursos.curselection()
        if selecionado:
            self.recursos.pop(selecionado[0])
            self.atualizar_lista()
            self.salvar_recursos()
        else:
            messagebox.showwarning(traduzir(self.idioma, 'titulo'), 'Por favor, selecione um recurso para remover.')

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
    app = GerenciadorRecursos(root, idioma='pt')
    root.mainloop()