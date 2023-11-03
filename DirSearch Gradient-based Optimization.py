"""
 Funções para teste:

 Booth: (x+2*y-7)**2+(2*x+y-5)**2 

 """
from sympy import symbols, diff, solve, Rational
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sympy as sym
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from fractions import Fraction
from scipy.optimize import minimize_scalar
from sympy import lambdify
import math
import re

def show_custom_dialog(x0, i):
    dialog = tk.Toplevel()
    dialog.title("Resultado")

    dialog.configure(bg="white")
    dialog.geometry("600x400")

    label = ttk.Label(dialog, text=f"Ponto ótimo: {x0}\nParou após {i} iterações", style="Custom.TLabel")
    label.pack(pady=20)

    button = ttk.Button(dialog, text="Fechar", command=dialog.destroy, style="Custom.TButton")
    button.pack()
    plt.show()

def plot_graficos(i, Lista_Pontos, funcao, Lista_Res, listagrad):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    # Curvas de Nível
    x1 = np.linspace(-80, 80, 200)
    x2 = np.linspace(-80, 80, 200)
    x, y = sym.symbols('x y')
    X, Y = np.meshgrid(x1, x2)
    Function = lambdify((x, y), funcao)
    Z = Function(X, Y)

    ax1.contour(X, Y, Z, levels=np.logspace(-80, 100, 200), colors="y")

    for j in range(i - 1):
        if j == i - 2:
            ax1.plot([Lista_Pontos[j][0], Lista_Pontos[j + 1][0]], [Lista_Pontos[j][1], Lista_Pontos[j + 1][1]], 'bo-')
            ax1.plot(Lista_Pontos[j + 1][0], Lista_Pontos[j + 1][1], 'r*', markersize=10)
            break
        else:
            ax1.plot([Lista_Pontos[j][0], Lista_Pontos[j + 1][0]], [Lista_Pontos[j][1], Lista_Pontos[j + 1][1]], 'bo-')

    x1 = np.linspace(-60, 60, 100)
    x2 = np.linspace(-60, 60, 100)
    X, Y = np.meshgrid(x1, x2)
    for j in range(len(Lista_Res)):
        Function = lambdify((x, y), Lista_Res[j])
        Z = Function(X, Y)
        ax1.contour(X, Y, Z, levels=[0, np.inf], colors='red', alpha=0.5, hatches=['.'])

    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_title('Curvas de nível e convergência')

    # Plot 3D
    x1 = np.linspace(-80, 80, 200)
    x2 = np.linspace(-80, 80, 200)
    x, y = sym.symbols('x y')
    X, Y = np.meshgrid(x1, x2)
    Function = lambdify((x, y), funcao)
    Z = Function(X, Y)

    ax2 = fig.add_subplot(132, projection='3d')
    ax2.plot_surface(X, Y, Z, cmap='coolwarm')

    for j in range(i - 2):
        if j == i - 3:
            ax2.plot(Lista_Pontos[j + 1][0], Lista_Pontos[j + 1][1], 'r*', markersize=10)
            break
        else:
            ax2.plot([Lista_Pontos[j][0], Lista_Pontos[j + 1][0]], [Lista_Pontos[j][1], Lista_Pontos[j + 1][1]], 'bo-')

    x1 = np.linspace(-60, 60, 100)
    x2 = np.linspace(-60, 60, 100)
    X, Y = np.meshgrid(x1, x2)
    for j in range(len(Lista_Res)):
        Function = lambdify((x, y), Lista_Res[j])
        Z = Function(X, Y)
        ax2.plot_surface(X, Y, Z, cmap='jet')

    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('3D')

    # Gráfico i vs. listagrad
    ax3.plot(range(i), listagrad)
    ax3.set_xlabel('iterações')
    ax3.set_ylabel('módulo do gradiente')
    ax3.set_title('Gráfico módulo do gradiente vs. iterações')

    plt.tight_layout()
    
    



def paradagradiente(n, Mg, Mmax):
    if n == 5:
        Mf = max(Mg)
        if Mf > (0.001 * Mmax):
            return 0
        else:
            print('parou')
            return 1
    else:
        return 0

def obter_funcao(texto,texto_x,texto_y,texto_R,var,var_Res):
    
    funcaoString = texto.get("1.0", tk.END)
    
    funcaoRes = texto_R.get("1.0", "end-1c")
    
    Lista_F=[] #Armazena a string da função
    Lista_Res=[] # Irá armazenar a(s) função(ões) de restrição após passar pela transformação
    Valores=[]
    TabelaRes=[]
    
    if funcaoRes.strip() != "":
        
     num_linhas = int(texto_R.index("end-1c").split(".")[0])
     print(num_linhas)
        
     for linha in range(1, num_linhas + 1):
            funcaoRes = texto_R.get(f"{linha}.0", f"{linha}.end")
            # Separar a string após "<" ou "<="
            padrao = r"<=|=|>"
            separado = re.split(padrao, funcaoRes)
            Res=separado[0]
            Valores.append(separado[1])
            padrao = r"(<=|=|>)(.*)"
            separado = re.findall(padrao, funcaoRes)
            
            TabelaRes.append(separado[0][0])
            print(f"Linha {linha}: {funcaoRes}")
            Lista_F.append(Res)
    
    
    x0 = [0, 0]
    try:
        x0[0] = float(Fraction(texto_x.get("1.0", tk.END).strip()))
        x0[1] = float(Fraction(texto_y.get("1.0", tk.END).strip()))

        funcao = sym.sympify(funcaoString)
       

        print("Função Digitada:", funcao)
        if len(Lista_F)!=0:
           
            print("Restrição(ões) sendo aplicada(s)")
            for i in range(len(Lista_F)):
                Fr= sym.sympify(Lista_F[i])
                if(TabelaRes[i]==">"):
                    Fr=-Fr+float(Fraction(Valores[i]))
                    TabelaRes[i]="<"
                else:
                    Fr=Fr-float(Fraction(Valores[i]))
                Lista_Res.append(Fr)
                print(f"{i+1}  --->  {Lista_Res[i]}{TabelaRes[i]} 0")
        

        x, y = sym.symbols('x y')
        df_dx = sym.diff(funcao, x)
        df_dy = sym.diff(funcao, y)
        gradient = [df_dx, df_dy]
        listagrad = []
        botaodepanico = 0
        antigargalo = 10000
        Mg = [0, 0, 0, 0, 0]
        point = {x: x0[0], y: x0[1]}
        gk = [g.subs(point) for g in gradient]
        Mmax = ((gk[0]**2) + (gk[1]**2))**0.5
        n = 0
        opcoes = ["Busca Aleatória", "Método do Gradiente"]
        metodo=var.get()
        
        Lista_Pontos=[]
        # Método da Busca aleatória
        if(metodo==opcoes[0]):

            m = np.random.rand(2, 1)
            d0 = [0, 0]
            d0[0] = m[0][0]
            d0[1] = m[1][0]

            i = 0
            while botaodepanico < antigargalo:
                
                Lista_Pontos.append([x0[0],x0[1]])
                
                parada = paradagradiente(n, Mg, Mmax)
                if parada == 1:
                    break
                if n == 5:
                    n = 0
                    point = {x: x0[0], y: x0[1]}
                gk = [g.subs(point) for g in gradient]
                gkmod = ((gk[0]**2) + (gk[1]**2))**0.5
                Mg[n] = gkmod
                listagrad.append(gkmod)
                
                
                
                a = symbols('a',real=True)
                x1 = [x0[0] + a*d0[0], x0[1] + a*d0[1]]

                funcao_substituida = funcao.subs([(x, x1[0]), (y, x1[1])])
                derivada_a = funcao_substituida.diff(a)

                a = solve(derivada_a, a)
                
                if len(a)==0: a=[1e-6]
                
                x0 = [x0[0] + a[0]*d0[0], x0[1] + a[0]*d0[1]]
                m = np.random.rand(2, 1)
                d0[0] = m[0][0]
                d0[1] = m[1][0]
                
                if not i%10:
                  print(x0)
                

                n += 1
                i += 1
                botaodepanico += 1

            
        #Método do Gradiente
        else:
            #Com Restrições
            funcao_new=funcao
            if var_Res=="Método das Penalidades":
                u=100
                for j in range(len(Lista_Res)):
                    
                    if TabelaRes[j]=="<=" or TabelaRes[j]=="<":
                        F=max(0,Lista_Res[j].subs({x: x0[0], y: x0[1]}))
                        if F!=0:
                            funcao_new=funcao_new+u*(Lista_Res[j])**2
                    else:
                        funcao_new=funcao_new+u*(Lista_Res[j])**2
               
                df_dx = sym.diff(funcao_new, x)
                df_dy = sym.diff(funcao_new, y)
                gradient = [df_dx, df_dy]
                i = 0
                
                while botaodepanico < antigargalo:
                    Lista_Pontos.append([x0[0],x0[1]])
                    
                    funcao_new=funcao
                    for j in range(len(Lista_Res)):
                        
                        if TabelaRes[j]=="<=" or TabelaRes[j]=="<" :
                            F=max(0,Lista_Res[j].subs({x: x0[0], y: x0[1]}))
                            if F!=0:
                                funcao_new=funcao_new+u*(Lista_Res[j])**2
                        else:
                            funcao_new=funcao_new+u*(Lista_Res[j])**2
                            
                    df_dx = sym.diff(funcao_new, x)
                    df_dy = sym.diff(funcao_new, y)
                    gradient = [df_dx, df_dy]
                    
                    parada = paradagradiente(n, Mg, Mmax)
                    if parada == 1:
                        break
                    if n == 5:
                        n = 0
                  
                    point = {x: x0[0], y: x0[1]}
                    gk = [g.subs(point) for g in gradient]
                    gkmod = ((gk[0]**2) + (gk[1]**2))**0.5
                    Mg[n] = gkmod
                    listagrad.append(gkmod)
                    a = symbols('a',real=True)
                    d0=[gk[0],gk[1]]
              
                    x1 = [x0[0] - a*d0[0], x0[1] - a*d0[1]]
              
                    F_alpha = funcao_new.subs([(x, x1[0]), (y, x1[1])])
                    F_alpha_lambda = lambdify(a, F_alpha)
              
                    def phi(alpha_val):
                      a=F_alpha_lambda(alpha_val)
                
                      return a
        
              
              #alfa mínimo
                    a = minimize_scalar(lambda a: phi(a), method='bounded', bounds=(0,1)).x
              
              # atualiza o x
              
                    x0 = [x0[0] - a*d0[0], x0[1] - a*d0[1]]
        
                    if not  i%10:
                      print(x0)

                    n += 1
                    i += 1
                    u=u*1.2
                    botaodepanico += 1
            
            
            #Método da Barreira
            else: 
                if var_Res == "Método da Barreira":
                    u=1000
                    for j in range(len(Lista_Res)):
                        
                        if TabelaRes[j]=="<=" or TabelaRes[j]=="<" : 
                         
                            funcao_new=funcao_new-u*(1/Lista_Res[j])
                        else:
                            funcao_new=funcao_new+u*(Lista_Res[j])**2
                    #print(funcao_new)    
                    df_dx = sym.diff(funcao_new, x)
                    df_dy = sym.diff(funcao_new, y)
                    gradient = [df_dx, df_dy]
                    i = 0
                    
                    while botaodepanico < antigargalo:
                        Lista_Pontos.append([x0[0],x0[1]])
                        
                        funcao_new=funcao
                        for j in range(len(Lista_Res)):
                            
                            if TabelaRes[j]=="<=" or TabelaRes[j]=="<" :
                                funcao_new=funcao_new-u*(1/Lista_Res[j])
                            else:
                                funcao_new=funcao_new+u*(Lista_Res[j])**2
                                
                        df_dx = sym.diff(funcao_new, x)
                        df_dy = sym.diff(funcao_new, y)
                        gradient = [df_dx, df_dy]
                        
                        parada = paradagradiente(n, Mg, Mmax)
                        if parada == 1:
                            break
                        if n == 5:
                            n = 0
                      
                        point = {x: x0[0], y: x0[1]}
                        gk = [g.subs(point) for g in gradient]
                        gkmod = ((gk[0]**2) + (gk[1]**2))**0.5
                        Mg[n] = gkmod
                        listagrad.append(gkmod)
                        a = symbols('a',real=True)
                        d0=[gk[0],gk[1]]
                  
                        x1 = [x0[0] - a*d0[0], x0[1] - a*d0[1]]
                  
                        F_alpha = funcao_new.subs([(x, x1[0]), (y, x1[1])])
                        F_alpha_lambda = lambdify(a, F_alpha)
                  
                        def phi(alpha_val):
                          a=F_alpha_lambda(alpha_val)
                    
                          return a
            
                  
                  #alfa mínimo
                        a = minimize_scalar(lambda a: phi(a), method='bounded', bounds=(0,1)).x
                  
                  # atualiza o x
                  
                        x0 = [x0[0] - a*d0[0], x0[1] - a*d0[1]]
            
                        if not  i%10:
                          print(x0)

                        n += 1
                        i += 1
                        u=u*0.9
                        botaodepanico += 1
             #Sem Restrições
                else:
                    i = 0
                    while botaodepanico < antigargalo:
                        Lista_Pontos.append([x0[0],x0[1]])
                        
                        parada = paradagradiente(n, Mg, Mmax)
                        if parada == 1:
                            break
                        if n == 5:
                            n = 0
                      
                        point = {x: x0[0], y: x0[1]}
                        gk = [g.subs(point) for g in gradient]
                        gkmod = ((gk[0]**2) + (gk[1]**2))**0.5
                        Mg[n] = gkmod
                        listagrad.append(gkmod)
    
                        a = symbols('a',real=True)
                        d0=[gk[0],gk[1]]
                  
                        x1 = [x0[0] - a*d0[0], x0[1] - a*d0[1]]
                  
                        F_alpha = funcao.subs([(x, x1[0]), (y, x1[1])])
                        F_alpha_lambda = lambdify(a, F_alpha)
                  
                        def phi(alpha_val):
                          a=F_alpha_lambda(alpha_val)
                    
                          return a
                  
                  #alfa mínimo
                        a = minimize_scalar(lambda a: phi(a), method='bounded', bounds=(0,1)).x
                  
                  # atualiza o x
                  
                        x0 = [x0[0] - a*d0[0], x0[1] - a*d0[1]]
            
                        if not  i%10:
                          print(x0)
    
                        n += 1
                        i += 1
                        botaodepanico += 1  

        print("ponto ótimo", x0)
        print("Parou após", i, "iterações")
        plot_graficos(i, Lista_Pontos, funcao, Lista_Res,listagrad)
        show_custom_dialog(x0, i)
        
    except Exception as e:
         messagebox.showerror("Erro!!!", "Ocorreu um erro. " + str(e) + " não é um valor válido! Por favor, verifique os valores inseridos.")
         texto_x.delete("1.0", tk.END)
         texto_y.delete("1.0", tk.END)

def menu():
    janela = tk.Tk()
    janela.title("Digite a Função")
    janela.geometry("600x700")

    style = ttk.Style()
    style.configure("TButton", padding=10, relief="flat", background="#2196f3", foreground="black", font=("Arial", 12))
    style.configure("TLabel", padding=10, font=("Arial", 12))
    style.configure("TEntry", padding=10, font=("Arial", 12))

    label_funcao = ttk.Label(janela, text="Digite a função:")
    label_funcao.pack()

    
    texto = tk.Text(janela, height=5, width=30)
    texto.pack()

    label_x = ttk.Label(janela, text="Digite o valor inicial x:")
    label_x.pack()

    texto_x = tk.Text(janela, height=1, width=10)
    texto_x.pack()

    label_y = ttk.Label(janela, text="Digite o valor inicial y:")
    label_y.pack()

    texto_y = tk.Text(janela, height=1, width=10)
    texto_y.pack(pady=(0, 20))
    
    label_R = ttk.Label(janela, text="Digite a(s) restrição(ões):")
    label_R.pack()

    texto_R = tk.Text(janela, height=5, width=40)
    texto_R.pack()

    label_metodo = ttk.Label(janela, text="Selecione um dos métodos de restrição:")
    label_metodo.pack()

    opcoes_Res = ["Método da Barreira", "Método das Penalidades", " Nenhum"]
    var_Res = tk.StringVar(janela)
    var_Res.set(opcoes_Res[0])  # Valor padrão exibido

    opcao_menu = tk.OptionMenu(janela, var_Res, *opcoes_Res)
    opcao_menu.pack(padx=20, pady=15)


    label_metodo = ttk.Label(janela, text="Selecione um dos métodos de busca:")
    label_metodo.pack()

    opcoes = ["Busca Aleatória", "Método do Gradiente"]
    var = tk.StringVar(janela)
    var.set(opcoes[0])  # Valor padrão exibido

    opcao_menu = tk.OptionMenu(janela, var, *opcoes)
    opcao_menu.pack(padx=20, pady=18)
    

    botao = ttk.Button(janela, text="Obter Ponto Ótimo", command=lambda :obter_funcao(texto,texto_x,texto_y,texto_R,var,var_Res))
    botao.pack(padx=20, pady=25)
    
    janela.mainloop()
    
menu()