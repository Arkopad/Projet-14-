import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class App():

    def __init__(self):
        
        self.racine = tk.Tk()
        self.racine.state("zoomed")
        self.racine.title("Paramètre")
        self.racine.configure(bg = "#222831")
        moniteurWidth = self.racine.winfo_screenwidth() # Largeur de l'écran
        moniteurHeight = self.racine.winfo_screenheight() # Hauteur de l'écran
        self.racine.geometry(f"1000x800+{moniteurWidth//2-500}+{moniteurHeight//2-400}")
        self.racine.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.largeur_silo_gauche = -1 #m
        self.largeur_silo_droite = 1 #m
        self.debut_du_trou = 0.7 #m en y
        # On définit les droites des parois des silos comme des droites de la forme y = Ax + C afin de mettre sous la forme -Ax + y - C = 0
        self.CoeffDir, self.OrdOrigine = -1/0.6, 0.5
        self.paroiGauche = lambda x : self.CoeffDir*x + self.OrdOrigine
        self.vecteur_directeur_paroi_gauche = np.array([1.0, self.CoeffDir])/ np.sqrt(1 + (self.CoeffDir)**2) #pointe vers le haut, normalisé
        self.vecteur_orthogonal_paroi_gauche = np.array([-self.CoeffDir, 1.0]) #pointe vers l'intérieur du silo, normalisé
        self.paroiDroite = lambda x : -self.CoeffDir*x + self.OrdOrigine
        self.vecteur_directeur_paroi_droite = np.array([1.0, -self.CoeffDir])/ np.sqrt(1 + (self.CoeffDir)**2) #pointe vers le haut, normalisé
        self.vecteur_orthogonal_paroi_droite = np.array([-self.CoeffDir, 1.0]) #pointe vers l'intérieur du silo, normalisé

        self.hauteur_bac = 0.4 #m
        self.largeurBac = 0.5 #m
    
        self.run = True

        self.creerWidgets()

    def on_closing(self):

        self.racine.destroy()
        self.racine.quit()

    def plot(self,canvas,ax):

        ax.clear()
        # dessin du silo dans le tableau graphique matplot
        # on trouve le x du debut du trou pour les deux parois:
        x_debut_du_trou_gauche = (self.debut_du_trou - self.OrdOrigine)/self.CoeffDir
        x_debut_du_trou_droite = (self.debut_du_trou - self.OrdOrigine)/-self.CoeffDir
        X1 = np.linspace(self.largeur_silo_gauche, x_debut_du_trou_gauche, 100)
        X2 = np.linspace(x_debut_du_trou_droite, self.largeur_silo_droite, 100)
        plt.plot(X1, self.paroiGauche(X1), color='#EEEEEE')
        plt.plot(X2, self.paroiDroite(X2), color='#EEEEEE')
        X3 = np.linspace(-self.largeurBac/2, self.largeurBac/2, 100)
        Y3 = np.zeros(100) + self.hauteur_bac
        plt.plot(X3, Y3, color='#EEEEEE')
        plt.grid()
        plt.tight_layout()                                          # On supprime les marges de la figure
        ax.set_aspect('equal')
        canvas.draw()

    def getParametres(self):
        """
        Récupère les paramètres du fichier parametres.csv
        :paramètres: self : la fenêtre racine
        :return:
        """
        try :                                                       # On essaye d'ouvrir le fichier parametres.csv     

            fichier = open("parametres.csv", "r+")                  # 

        except FileNotFoundError:                                   # Si le fichier n'existe pas

            fichier = open("parametres.csv", "w+")                  # On le crée
            fichier.close()                                         # On le ferme
            fichier = open("parametres.csv", "r+")                  # On le réouvre en lecture

        parametres = fichier.read().split(";")                      # On lit le fichier et on récupère les paramètres
        fichier.close()                                             # On ferme le fichier

        if parametres == ['']:                                      # Si le fichier est vide
            
            parametres = ["-1.6667", "0.5", "0.7", "0.5", "0.4"]   # On initialise les paramètres

        try:                                                        # On essaye de convertir les paramètres en entier

            self.CoeffDir = float(parametres[0])                          # On récupère les paramètres
            self.OrdOrigine = float(parametres[1])                        # 
            self.debut_du_trou = float(parametres[2])                     #
            self.largeurBac = float(parametres[3])                        #
            self.hauteur_bac = float(parametres[4])                       #
        
        except Exception as erreur:                                 # Si les paramètres ne sont pas des entiers
            
            print("Erreur : le fichier parametres.csv est corrompu, les paramètres ont été réinitialisés\nDétail de l'erreur : ", erreur)   # On affiche un message d'erreur
            parametres = ["-1.6667", "0.5", "0.7", "0.5", "0.4"]            # On initialise les paramètres
            fichier = open("parametres.csv", "w+")                  # On ouvre le fichier en écriture
            fichier.write(";".join(parametres))                     # On écrit les paramètres dans le fichier
            fichier.close()                                         # On ferme le fichier
            self.getParametres()                                    # On rappelle la fonction pour récupérer les paramètres


    def save(self, *event):
        """
        Sauvegarde les paramètres dans le fichier parametres.csv
        :paramètres:
        :return:
        """
        fichier = open("parametres.csv", "w+")          # On ouvre le fichier parametres.csv en écriture et on le crée s'il n'existe pas et on écrit les paramètres dedans
        fichier.write("{CoeffDir};{OrdOrigine};{debut_du_trou};{largeurBac};{hauteur_bac}".format(CoeffDir = self.CoeffDir, 
                                                                                                  OrdOrigine = self.OrdOrigine, 
                                                                                                  debut_du_trou = self.debut_du_trou, 
                                                                                                  largeurBac = self.largeurBac, 
                                                                                                  hauteur_bac = self.hauteur_bac))
        fichier.close()                                 # On ferme le fichier
        self.kill()
    
    def kill(self, *event):

        self.run = False
        self.racine.destroy()
        self.racine.quit()

    def creerWidgets(self):
        
        self.getParametres()
        # create label for game options
        options_label = tk.Label(self.racine, text="Paramètre de la modélisation", font="Lucida 16 bold", bg = '#393E46', fg= '#EEEEEE', pady=10)
        options_label.pack(side=tk.TOP, fill='x')

        # create label for number of players
        CoeffDirLabel = tk.Label(self.racine, text="Coeff. dir.:", font="Lucida 10 bold", bg = '#222831', fg= '#EEEEEE')
        CoeffDirLabel.pack(side=tk.TOP, fill='x')

        validateButton = tk.Button(self.racine, text="Enregistrer", bg = '#D65A31', fg= '#EEEEEE', bd=0, font ='Lucida 16 bold', command=self.save)
        validateButton.pack(side=tk.BOTTOM, fill='x')
        
        def setCoeffDir(*event):   

            self.CoeffDir = CoeffDirScale.get()/10
            self.canvas.draw()
            self.plot(self.canvas, self.ax)


        # create scrolled text for the number of the joueurs
        CoeffDirScale = tk.Scale(self.racine, from_=-100, to=-1, orient='horizontal', font="Lucida 10 bold", bg = '#222831', fg= '#EEEEEE', relief='flat', highlightthickness=0, troughcolor='#393E46', command= setCoeffDir,resolution=0.001)
        CoeffDirScale.set(self.CoeffDir*10)
        CoeffDirScale.pack(side=tk.TOP, fill='x')

        OrdOrigineLabel = tk.Label(self.racine, text="Ord. origine:", font="Lucida 10 bold", bg = '#222831', fg= '#EEEEEE')
        OrdOrigineLabel.pack(side=tk.TOP, fill='x')

        def setOrdOrigine(*event):   

            self.OrdOrigine = OrdOrigineScale.get()/10
            self.canvas.draw()
            self.plot(self.canvas, self.ax)

        # create scrolled text for the number of the joueurs
        OrdOrigineScale = tk.Scale(self.racine, from_=-100, to=100, orient='horizontal', font="Lucida 10 bold", bg = '#222831', fg= '#EEEEEE', relief='flat', highlightthickness=0, troughcolor='#393E46', command=setOrdOrigine,resolution=0.001)
        OrdOrigineScale.set(self.OrdOrigine*10)
        OrdOrigineScale.pack(side=tk.TOP, fill='x')

        debutTrouLabel = tk.Label(self.racine, text="Ord. début trou:", font="Lucida 10 bold", bg = '#222831', fg= '#EEEEEE')
        debutTrouLabel.pack(side=tk.TOP, fill='x')

        def setDebutTrou(*event):   

            self.debut_du_trou = debutTrouScale.get()/10
            self.ax.clear()
            self.plot(self.canvas, self.ax)
            self.canvas.draw()

        # create scrolled text for the number of the manche
        debutTrouScale = tk.Scale(self.racine, from_=0, to=100, orient='horizontal', font="Lucida 10 bold", bg = '#222831', fg= '#EEEEEE', relief='flat', highlightthickness=0, troughcolor='#393E46', command=setDebutTrou,resolution=0.001)
        debutTrouScale.set(self.debut_du_trou*10)
        debutTrouScale.pack(side=tk.TOP, fill='x')

        LargeurBacLabel = tk.Label(self.racine, text="Largeur bac droit:", font="Lucida 10 bold", bg = '#222831', fg= '#EEEEEE')
        LargeurBacLabel.pack(side=tk.TOP, fill='x')

        def setLargeurBac(*event):   

            self.largeurBac = LargeurBacScale.get()/10
            self.ax.clear()
            self.plot(self.canvas, self.ax)
            self.canvas.draw()

        # create scrolled text for the number of the manche
        LargeurBacScale = tk.Scale(self.racine, from_=0, to=100, orient='horizontal', font="Lucida 10 bold", bg = '#222831', fg= '#EEEEEE', relief='flat', highlightthickness=0, troughcolor='#393E46', command=setLargeurBac,resolution=0.001)
        LargeurBacScale.set(self.largeurBac*10)
        LargeurBacScale.pack(side=tk.TOP, fill='x')

        HauteurBacLabel = tk.Label(self.racine, text="Hauteur bac:", font="Lucida 10 bold", bg = '#222831', fg= '#EEEEEE')
        HauteurBacLabel.pack(side=tk.TOP, fill='x')

        def setHauteurBac(*event):   

            self.hauteur_bac = HauteurBacScale.get()/10
            self.ax.clear()
            self.plot(self.canvas, self.ax)
            self.canvas.draw()

        # create scrolled text for the number of the manche
        HauteurBacScale = tk.Scale(self.racine, from_=-100, to=100, orient='horizontal', font="Lucida 10 bold", bg = '#222831', fg= '#EEEEEE', relief='flat', highlightthickness=0, troughcolor='#393E46', command=setHauteurBac,resolution=0.001)
        HauteurBacScale.set(self.hauteur_bac*10)
        HauteurBacScale.pack(side=tk.TOP, fill='x')


        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.fig.patch.set_facecolor('#222831')                          # On définit la couleur de fond de la figure
        self.ax.set_facecolor('#222831')                          # On définit la couleur de fond de la figure
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('#EEEEEE')
        self.ax.grid(alpha=0.1)
        # dessin du silo dans le tableau graphique matplot
        # on trouve le x du debut du trou pour les deux parois:
        x_debut_du_trou_gauche = (self.debut_du_trou - self.OrdOrigine)/self.CoeffDir
        x_debut_du_trou_droite = (self.debut_du_trou - self.OrdOrigine)/self.CoeffDir
        X1 = np.linspace(self.largeur_silo_gauche, x_debut_du_trou_gauche, 100)
        X2 = np.linspace(x_debut_du_trou_droite, self.largeur_silo_droite, 100)
        plt.plot(X1, self.paroiGauche(X1), color='#EEEEEE')
        plt.plot(X2, self.paroiDroite(X2), color='#EEEEEE')
        X3 = np.linspace(-self.largeurBac/2, self.largeurBac/2, 100)
        Y3 = np.zeros(100) + self.hauteur_bac
        plt.plot(X3, Y3, color='#EEEEEE')
        plt.grid()
        plt.tight_layout()                                          # On supprime les marges de la figure

        self.canvas=FigureCanvasTkAgg(self.fig, master=self.racine)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill='x')
        self.canvas.draw()

app = App()
app.racine.mainloop()