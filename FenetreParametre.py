### Projet GéoQuiz ###

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class App():

    def __init__(self):

        self.largeur_silo_gauche = -1 #m
        self.largeur_silo_droite = 1 #m
        self.debut_du_trou = 0.7 #m en y
        # On définit les droites des parois des silos comme des droites de la forme y = Ax + C afin de mettre sous la forme -Ax + y - C = 0
        self.Agauche, self.Cgauche = -1/0.6, 0.5
        self.paroiGauche = lambda x : self.Agauche*x + self.Cgauche
        self.vecteur_directeur_paroi_gauche = np.array([1.0, self.Agauche])/ np.sqrt(1 + (self.Agauche)**2) #pointe vers le haut, normalisé
        self.vecteur_orthogonal_paroi_gauche = np.array([-self.Agauche, 1.0]) #pointe vers l'intérieur du silo, normalisé
        self.Adroite, self.Cdroite = 1/0.6, 0.5
        self.paroiDroite = lambda x : self.Adroite*x+self.Cdroite
        self.vecteur_directeur_paroi_droite = np.array([1.0, self.Adroite])/ np.sqrt(1 + (self.Agauche)**2) #pointe vers le haut, normalisé
        self.vecteur_orthogonal_paroi_droite = np.array([-self.Adroite, 1.0]) #pointe vers l'intérieur du silo, normalisé

        self.hauteur_bac = 0.4 #m
        self.largeur_bac_gauche = 0.5 #m
        self.largeur_bac_droite = 0.5 #m

        self.creerWidgets()
    
    def plot(self,canvas,ax):


        ax.clear()
        # dessin du silo dans le tableau graphique matplot
        # on trouve le x du debut du trou pour les deux parois:
        x_debut_du_trou_gauche = (self.debut_du_trou - self.Cgauche)/self.Agauche
        x_debut_du_trou_droite = (self.debut_du_trou - self.Cdroite)/self.Adroite
        X1 = np.linspace(self.largeur_silo_gauche, x_debut_du_trou_gauche, 100)
        X2 = np.linspace(x_debut_du_trou_droite, self.largeur_silo_droite, 100)
        plt.plot(X1, self.paroiGauche(X1), color='black')
        plt.plot(X2, self.paroiDroite(X2), color='black')
        X3 = np.linspace(-self.largeur_bac_gauche, self.largeur_bac_droite, 100)
        Y3 = np.zeros(100) + self.hauteur_bac
        plt.plot(X3, Y3, color='black')
        plt.grid()
        plt.tight_layout()                                          # On supprime les marges de la figure
        ax.set_aspect('equal')
        canvas.draw()

    def creerWidgets(self):

        self.racine = tk.Tk()
        self.racine.state("zoomed")
        self.racine.title("Paramètre")
        self.racine.configure(bg = "#557171")
        moniteurWidth = self.racine.winfo_screenwidth() # Largeur de l'écran
        moniteurHeight = self.racine.winfo_screenheight() # Hauteur de l'écran
        self.racine.geometry(f"1000x800+{moniteurWidth//2-500}+{moniteurHeight//2-400}")
        self.racine.protocol("WM_DELETE_WINDOW", self.racine.destroy)

        # create label for game options
        options_label = tk.Label(self.racine, text="Paramètre de la modélisation", font="Lucida 10 bold", bg = '#3E5151', fg= '#FFFFFF', pady=10)
        options_label.pack(side=tk.TOP, fill='x')

        # create label for number of players
        AgaucheLabel = tk.Label(self.racine, text="Coeff. dir. gauche:", font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF')
        AgaucheLabel.pack(side=tk.TOP, fill='x')

        def setAgauche(*event):   

            self.Agauche = AgaucheScale.get()/10
            self.canvas.draw()
            self.plot(self.canvas, self.ax)


        # create scrolled text for the number of the joueurs
        AgaucheScale = tk.Scale(self.racine, from_=-100, to=-1, orient='horizontal', font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF', relief='flat', highlightthickness=0, troughcolor='#698F8E', command= setAgauche)
        AgaucheScale.set(self.Agauche*10)
        AgaucheScale.pack(side=tk.TOP, fill='x')

        AdroiteLabel = tk.Label(self.racine, text="Coeff. dir. droite:", font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF')
        AdroiteLabel.pack(side=tk.TOP, fill='x')

        def setAdroite(*event):   

            self.Adroite = AdroiteScale.get()/10
            self.canvas.draw()
            self.plot(self.canvas, self.ax)

        # create scrolled text for the number of the joueurs
        AdroiteScale = tk.Scale(self.racine, from_=1, to=100, orient='horizontal', font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF', relief='flat', highlightthickness=0, troughcolor='#698F8E', command=setAdroite)
        AdroiteScale.set(self.Adroite*10)
        AdroiteScale.pack(side=tk.TOP, fill='x')

        CgaucheLabel = tk.Label(self.racine, text="Ord. origine gauche:", font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF')
        CgaucheLabel.pack(side=tk.TOP, fill='x')

        def setCgauche(*event):   

            self.Cgauche = CgaucheScale.get()/10
            self.canvas.draw()
            self.plot(self.canvas, self.ax)

        # create scrolled text for the number of the joueurs
        CgaucheScale = tk.Scale(self.racine, from_=-100, to=100, orient='horizontal', font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF', relief='flat', highlightthickness=0, troughcolor='#698F8E', command=setCgauche)
        CgaucheScale.set(self.Cgauche*10)
        CgaucheScale.pack(side=tk.TOP, fill='x')

        CdroiteLabel = tk.Label(self.racine, text="Ord. origine droite:", font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF')
        CdroiteLabel.pack(side=tk.TOP, fill='x')

        def setCdroite(*event):   

            self.Cdroite = CdroiteScale.get()/10
            self.canvas.draw()
            self.plot(self.canvas, self.ax)

        # create scrolled text for the number of the joueurs
        CdroiteScale = tk.Scale(self.racine, from_=-100, to=100, orient='horizontal', font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF', relief='flat', highlightthickness=0, troughcolor='#698F8E', command=setCdroite)
        CdroiteScale.set(self.Cdroite*10)
        CdroiteScale.pack(side=tk.TOP, fill='x')


        debutTrouLabel = tk.Label(self.racine, text="Ord. début trou:", font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF')
        debutTrouLabel.pack(side=tk.TOP, fill='x')

        def setDebutTrou(*event):   

            self.debut_du_trou = debutTrouScale.get()/10
            self.ax.clear()
            self.plot(self.canvas, self.ax)
            self.canvas.draw()

        # create scrolled text for the number of the manche
        debutTrouScale = tk.Scale(self.racine, from_=0, to=100, orient='horizontal', font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF', relief='flat', highlightthickness=0, troughcolor='#698F8E', command=setDebutTrou)
        debutTrouScale.set(self.debut_du_trou*10)
        debutTrouScale.pack(side=tk.TOP, fill='x')



        LargeurBacDroiteLabel = tk.Label(self.racine, text="Largeur bac droit:", font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF')
        LargeurBacDroiteLabel.pack(side=tk.TOP, fill='x')

        def setLargeurBacDroite(*event):   

            self.largeur_bac_droite = LargeurBacDroiteScale.get()/10
            self.ax.clear()
            self.plot(self.canvas, self.ax)
            self.canvas.draw()

        # create scrolled text for the number of the manche
        LargeurBacDroiteScale = tk.Scale(self.racine, from_=-100, to=100, orient='horizontal', font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF', relief='flat', highlightthickness=0, troughcolor='#698F8E', command=setLargeurBacDroite)
        LargeurBacDroiteScale.set(self.largeur_bac_droite*10)
        LargeurBacDroiteScale.pack(side=tk.TOP, fill='x')


        LargeurBacGaucheLabel = tk.Label(self.racine, text="Largeur bac gauche:", font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF')
        LargeurBacGaucheLabel.pack(side=tk.TOP, fill='x')

        def setLargeurBacGauche(*event):   

            self.largeur_bac_gauche = LargeurBacGaucheScale.get()/10
            self.ax.clear()
            self.plot(self.canvas, self.ax)
            self.canvas.draw()

        # create scrolled text for the number of the manche
        LargeurBacGaucheScale = tk.Scale(self.racine, from_=-100, to=100, orient='horizontal', font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF', relief='flat', highlightthickness=0, troughcolor='#698F8E', command=setLargeurBacGauche)
        LargeurBacGaucheScale.set(self.largeur_bac_gauche*10)
        LargeurBacGaucheScale.pack(side=tk.TOP, fill='x')



        HauteurBacLabel = tk.Label(self.racine, text="Hauteur bac:", font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF')
        HauteurBacLabel.pack(side=tk.TOP, fill='x')

        def setHauteurBac(*event):   

            self.hauteur_bac = HauteurBacScale.get()/10
            self.ax.clear()
            self.plot(self.canvas, self.ax)
            self.canvas.draw()

        # create scrolled text for the number of the manche
        HauteurBacScale = tk.Scale(self.racine, from_=-100, to=100, orient='horizontal', font="Lucida 10 bold", bg = '#557171', fg= '#FFFFFF', relief='flat', highlightthickness=0, troughcolor='#698F8E', command=setHauteurBac)
        HauteurBacScale.set(self.hauteur_bac*10)
        HauteurBacScale.pack(side=tk.TOP, fill='x')


        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.fig.patch.set_facecolor('#557171')                          # On définit la couleur de fond de la figure
        # dessin du silo dans le tableau graphique matplot
        # on trouve le x du debut du trou pour les deux parois:
        x_debut_du_trou_gauche = (self.debut_du_trou - self.Cgauche)/self.Agauche
        x_debut_du_trou_droite = (self.debut_du_trou - self.Cdroite)/self.Adroite
        X1 = np.linspace(self.largeur_silo_gauche, x_debut_du_trou_gauche, 100)
        X2 = np.linspace(x_debut_du_trou_droite, self.largeur_silo_droite, 100)
        plt.plot(X1, self.paroiGauche(X1), color='black')
        plt.plot(X2, self.paroiDroite(X2), color='black')
        X3 = np.linspace(-self.largeur_bac_gauche, self.largeur_bac_droite, 100)
        Y3 = np.zeros(100) + self.hauteur_bac
        plt.plot(X3, Y3, color='black')
        plt.grid()
        plt.tight_layout()                                          # On supprime les marges de la figure

        self.canvas=FigureCanvasTkAgg(self.fig, master=self.racine)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill='x')
        self.canvas.draw()

        validateButton = tk.Button(self.racine, text="Enregistrer", bg = '#98C8C2', fg= '#FFFFFF', bd=0, font ='Lucida 16 bold', command=self.racine.destroy)
        validateButton.pack(side=tk.BOTTOM, fill='x')


if __name__ == "__main__":

    app = App()
    app.racine.mainloop()