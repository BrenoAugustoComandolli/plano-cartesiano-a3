import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

class PlanoCartesianoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Plano Cartesiano")
        
        self.dark_mode = tk.BooleanVar(value=True)
        
        self.tela = ttk.Frame(self.root, padding="20")
        self.tela.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.label_x = ttk.Label(self.tela, text="Coordenada X:")
        self.label_x.grid(column=0, row=0, sticky=(tk.W, tk.E), pady=[0, 10])
        
        self.entry_x = ttk.Entry(self.tela)
        self.entry_x.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=[0, 10])
        
        self.label_y = ttk.Label(self.tela, text="Coordenada Y:")
        self.label_y.grid(column=0, row=1, sticky=(tk.W, tk.E))
        
        self.entry_y = ttk.Entry(self.tela)
        self.entry_y.grid(column=1, row=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.botao_adicionar = ttk.Button(self.tela, text="Adicionar Ponto", command=self.adicionar_ponto)
        self.botao_adicionar.grid(column=0, row=2, columnspan=2, sticky=(tk.W, tk.E), pady=[10, 10])

        self.botao_remover = ttk.Button(self.tela, text="Remover Ponto", command=self.remover_ponto)
        self.botao_remover.grid(column=0, row=3, columnspan=2, sticky=(tk.W, tk.E), pady=[0, 10])
        
        self.treeview = ttk.Treeview(self.tela, columns=("X", "Y"), show='headings', selectmode='extended')
        self.treeview.heading("X", text="X")
        self.treeview.heading("Y", text="Y")
        
        self.treeview.column("X", anchor=tk.CENTER)
        self.treeview.column("Y", anchor=tk.CENTER)
        
        self.treeview.grid(column=0, row=4, columnspan=2, sticky=(tk.W, tk.E))

        self.botao_plotar = ttk.Button(self.tela, text="Gerar Gráfico", command=self.criar_grafico)
        self.botao_plotar.grid(column=0, row=5, columnspan=2, sticky=(tk.W, tk.E), pady=[10, 0])
        
        dark_ativado = Image.open("assets/dark-ativado.png")
        dark_ativado = dark_ativado.resize((20, 20))
        self.dark_ativado = ImageTk.PhotoImage(dark_ativado)
        self.botao_modo = ttk.Button(self.tela, text="", command=self.alternar_modo)
        self.botao_modo.grid(column=0, row=6, columnspan=1, sticky=(tk.W, tk.E), pady=[10, 10])
        self.botao_modo.configure(text='', image=self.dark_ativado, compound=tk.LEFT)

        # Aplicando o modo escuro na interface Tkinter
        self.aplicar_dark_mode(self.root)

    def adicionar_ponto(self):
        x = self.entry_x.get()
        y = self.entry_y.get()
        if x and y:
            self.treeview.insert("", "end", values=(x, y))
            self.entry_x.delete(0, tk.END)
            self.entry_y.delete(0, tk.END)
    
    def remover_ponto(self):
        selected_items = self.treeview.selection()
        for selected_item in selected_items:
            self.treeview.delete(selected_item)
    
    def criar_grafico(self):
        pontos_x = []
        pontos_y = []
        
        for item in self.treeview.get_children():
            valores = self.treeview.item(item, "values")
            pontos_x.append(float(valores[0]))
            pontos_y.append(float(valores[1]))
        
        if len(pontos_x) < 2 or len(pontos_y) < 2:
            messagebox.showinfo("Erro", "Adicione pelo menos dois pontos.")
            return
        
        limites_x = [min(pontos_x) - 1, max(pontos_x) + 1]
        limites_y = [min(pontos_y) - 1, max(pontos_y) + 1]
        
        # Configurando o modo escuro ou claro para o Matplotlib
        plt.style.use('dark_background' if self.dark_mode.get() else 'default')
        
        plt.figure()
        plt.scatter(pontos_x, pontos_y, color='red', label='Pontos')
        plt.plot(pontos_x, pontos_y, color='green', label='Linhas')
        plt.xlabel('Eixo X', color='white' if self.dark_mode.get() else 'black')
        plt.ylabel('Eixo Y', color='white' if self.dark_mode.get() else 'black')
        plt.title('Plano Cartesiano', color='white' if self.dark_mode.get() else 'black')
        plt.grid(True, color='gray')
        
        plt.axhline(0, color='white' if self.dark_mode.get() else 'black', linewidth=0.5)
        plt.axvline(0, color='white' if self.dark_mode.get() else 'black', linewidth=0.5)
        
        plt.xlim(limites_x)
        plt.ylim(limites_y)
        
        plt.legend()
        plt.show()

    def aplicar_dark_mode(self, widget):
        widget.tk_setPalette(background='#2e2e2e', foreground='white', activeBackground='#3e3e3e', activeForeground='white')
        for child in widget.winfo_children():
            if isinstance(child, ttk.Frame) or isinstance(child, ttk.Label) or isinstance(child, ttk.Button):
                child.configure(style='Dark.TFrame' if isinstance(child, ttk.Frame) else 'Dark.TLabel' if isinstance(child, ttk.Label) else 'Dark.TButton')
            elif isinstance(child, ttk.Entry):
                child.configure(background='white', foreground='black')
            self.aplicar_dark_mode(child)

    def aplicar_light_mode(self, widget):
        widget.tk_setPalette(background='white', foreground='black', activeBackground='#e0e0e0', activeForeground='black')
        for child in widget.winfo_children():
            if isinstance(child, ttk.Frame) or isinstance(child, ttk.Label) or isinstance(child, ttk.Button):
                child.configure(style='Light.TFrame' if isinstance(child, ttk.Frame) else 'Light.TLabel' if isinstance(child, ttk.Label) else 'Light.TButton')
            elif isinstance(child, ttk.Entry):
                child.configure(background='white', foreground='black')
            self.aplicar_light_mode(child)

    def alternar_modo(self):
        if self.dark_mode.get():
            dark_desativado = Image.open("assets/dark-desativado.png")
            dark_desativado = dark_desativado.resize((20, 20))
            self.dark_desativado = ImageTk.PhotoImage(dark_desativado)
            self.botao_modo.configure(text='', image=self.dark_desativado, compound=tk.LEFT)
            self.aplicar_light_mode(self.root)
            self.dark_mode.set(False)
        else:
            dark_ativado = Image.open("assets/dark-ativado.png")
            dark_ativado = dark_ativado.resize((20, 20))
            self.dark_ativado = ImageTk.PhotoImage(dark_ativado)
            self.botao_modo.configure(text='', image=self.dark_ativado, compound=tk.LEFT)
            self.aplicar_dark_mode(self.root)
            self.dark_mode.set(True)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure('Dark.TFrame', background='#2e2e2e')
    style.configure('Dark.TLabel', background='#2e2e2e', foreground='white')
    style.configure('Dark.TEntry', fieldbackground='white', foreground='black')
    style.configure('Dark.TButton', background='#3e3e3e', foreground='black')

    style.configure('Light.TFrame', background='white')
    style.configure('Light.TLabel', background='white', foreground='black')
    style.configure('Light.TEntry', fieldbackground='white', foreground='black')
    style.configure('Light.TButton', background='#e0e0e0', foreground='black')
    
    app = PlanoCartesianoApp(root)
    root.mainloop()