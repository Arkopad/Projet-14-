import tkinter as tk
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
        self.limite_bas = -1  #m
        self.limite_haut = 2 #m
        self.limite_gauche = -1 #m
        self.limite_droite = 1 #m
        self.largeur_silo_gauche = -1 #m
        self.largeur_silo_droite = 1 #m
        self.debutTrou = 0.7 #m en y
        # On définit les droites des parois des silos comme des droites de la forme y = Ax + C afin de mettre sous la forme -Ax + y - C = 0
        self.CoeffDir, self.OrdOrigine = -1/0.6, 0.5
        self.paroiGauche = lambda x : self.CoeffDir*x + self.OrdOrigine
        self.vecteur_directeur_paroi_gauche = np.array([1.0, self.CoeffDir])/ np.sqrt(1 + (self.CoeffDir)**2) #pointe vers le haut, normalisé
        self.vecteur_orthogonal_paroi_gauche = np.array([-self.CoeffDir, 1.0]) #pointe vers l'intérieur du silo, normalisé
        self.paroiDroite = lambda x : -self.CoeffDir*x + self.OrdOrigine
        self.vecteur_directeur_paroi_droite = np.array([1.0, -self.CoeffDir])/ np.sqrt(1 + (self.CoeffDir)**2) #pointe vers le haut, normalisé
        self.vecteur_orthogonal_paroi_droite = np.array([-self.CoeffDir, 1.0]) #pointe vers l'intérieur du silo, normalisé
        self.hauteur = 1.5
        self.hauteurBac = 0.4 #m
        self.largeurBac = 0.5 #m

        self.rayon = 6e-3 #m
        self.nbGrains = 100
    
        self.run = True

        self.displayGrain = tk.IntVar()

        self.creerWidgets()

    def on_closing(self):

        self.racine.destroy()
        self.racine.quit()

    def plot(self,canvas,ax):

        ax.clear()
        # dessin du silo dans le tableau graphique matplot
        # on trouve le x du debut du trou pour les deux parois:
        self.limite_bas = self.hauteurBac - 0.01
        x_debutTrou_gauche = (self.debutTrou - self.OrdOrigine)/self.CoeffDir
        x_debutTrou_droite = (self.debutTrou - self.OrdOrigine)/-self.CoeffDir
        X1 = np.linspace(self.largeur_silo_gauche, x_debutTrou_gauche, 100)
        X2 = np.linspace(x_debutTrou_droite, self.largeur_silo_droite, 100)
        plt.plot(X1, self.paroiGauche(X1), color='#EEEEEE')
        plt.plot(X2, self.paroiDroite(X2), color='#EEEEEE')
        X3 = np.linspace(-self.largeurBac/2, self.largeurBac/2, 100)
        Y3 = np.zeros(100) + self.hauteurBac
        plt.plot(X3, Y3, color='#EEEEEE')

        if self.displayGrain.get():

            self.gauche = (self.hauteur - self.OrdOrigine)/self.CoeffDir + self.rayon*1.3
            self.droite = (self.hauteur - self.OrdOrigine)/-self.CoeffDir - self.rayon*1.3

            POSITION = np.zeros((1, self.nbGrains, 2))   
            grain = 0 # compteur grain
            q = 0 # compteur colonne

            while grain < self.nbGrains:
                while True:
                    x = self.gauche + (self.rayon*1.3*2)*q
                    y = self.hauteur
                    if x > self.droite or grain >= self.nbGrains:
                        break
                    else:
                        POSITION[0, grain, 0] = x
                        POSITION[0, grain, 1] = y
                        grain += 1
                        q += 1
                if grain < self.nbGrains:
                    q = 0
                    self.hauteur -= self.rayon*1.3*2
                    self.gauche = (self.hauteur - self.OrdOrigine)/self.CoeffDir + self.rayon*1.3
                    self.droite = (self.hauteur - self.OrdOrigine)/-self.CoeffDir - self.rayon*1.3
                    x = self.gauche + (self.rayon*1.3*2)*q
                    y = self.hauteur
                    POSITION[0, grain, 0] = x
                    POSITION[0, grain, 1] = y
                    grain += 1
                    q += 1
                else:
                    break

            for i in range(len(POSITION[0])):
                
                plt.scatter(POSITION[0][i][0], POSITION[0][i][1], s=self.rayon*200, marker='o', c='red')
        #ax.add_patch(Rectangle(self.boite_grains[0],self.boite_grains[1], self.boite_grains[2], facecolor = 'red'))

        plt.xlim([self.limite_gauche, self.limite_droite])
        plt.ylim([self.limite_bas, self.limite_haut])
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
            
            parametres = ["-1.6667", "0.5", "0.7", "0.5", "0.4", "50","1.5"]   # On initialise les paramètres

        try:                                                        # On essaye de convertir les paramètres en entier

            self.CoeffDir = float(parametres[0])                          # On récupère les paramètres
            self.OrdOrigine = float(parametres[1])                        # 
            self.debutTrou = float(parametres[2])                     #
            self.largeurBac = float(parametres[3])                        #
            self.hauteurBac = float(parametres[4])                       #
            self.nbGrains = float(parametres[5])
            self.hauteur = float(parametres[6])
        
        except Exception as erreur:                                 # Si les paramètres ne sont pas des entiers
            
            print("Erreur : le fichier parametres.csv est corrompu, les paramètres ont été réinitialisés\nDétail de l'erreur : ", erreur)   # On affiche un message d'erreur
            parametres = ["-1.6667", "0.5", "0.7", "0.5", "0.4", "50","1.5"]            # On initialise les paramètres
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
        print("zz")
        fichier = open("parametres.csv", "w+")          # On ouvre le fichier parametres.csv en écriture et on le crée s'il n'existe pas et on écrit les paramètres dedans
        fichier.write("{CoeffDir};{OrdOrigine};{debutTrou};{largeurBac};{hauteurBac}".format(CoeffDir = self.CoeffDir, 
                                                                                                  OrdOrigine = self.OrdOrigine, 
                                                                                                  debutTrou = self.debutTrou, 
                                                                                                  largeurBac = self.largeurBac, 
                                                                                                  hauteurBac = self.hauteurBac))
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

        def setCoeffDir(*event):   

            self.displayGrain.set(0)
            try:
                if CoeffDirEntry.get() != '':
                    CoeffDirScale.set(float(CoeffDirEntry.get())*10000)
                self.CoeffDir = CoeffDirScale.get()/10000
            except Exception as e:
                print(f"Valeur de Coeff dir non valide : {e}")
            CoeffDirEntry.delete(0,tk.END)
            CoeffDirEntry.insert(0,'')
            self.canvas.draw()
            self.plot(self.canvas, self.ax)

        CoeffDirFrame = tk.Frame(self.racine, bd=0, bg = '#222831')
        CoeffDirFrame.pack(side=tk.TOP, pady=(10,0))

        CoeffDirLabel = tk.Label(CoeffDirFrame, text="Coeff. dir. (x10000):", font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE')
        CoeffDirLabel.grid(row=0, column=0)

        CoeffDirEntry = tk.Entry(CoeffDirFrame, bd=0 ,font="Lucida 11 bold", bg = '#EEEEEE', fg= '#222831')
        CoeffDirEntry.grid(row=0, column=1)

        CoeffDirValidateButton = tk.Button(CoeffDirFrame, bd=0, cursor="hand2", text = "Valider", font="Lucida 11 bold", bg = '#393E46', fg= '#EEEEEE', command=setCoeffDir)
        CoeffDirValidateButton.grid(row=0, column=2)

        # create scrolled text for the number of the joueurs
        CoeffDirScale = tk.Scale(self.racine, from_=-100000, to=-1, orient='horizontal', font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE', relief='flat', highlightthickness=0, troughcolor='#393E46', command= setCoeffDir)
        CoeffDirScale.set(self.CoeffDir*10000)
        CoeffDirScale.pack(side=tk.TOP, padx=20, fill='x')

        def setOrdOrigine(*event):   
            
            self.displayGrain.set(0)
            try:
                if OrdOrigineEntry.get() != '':
                    OrdOrigineScale.set(float(OrdOrigineEntry.get())*10000)
                self.OrdOrigine = OrdOrigineScale.get()/10000
            except Exception as e:
                print(f"Valeur de Ord Origine dir non valide : {e}")
            OrdOrigineEntry.delete(0,tk.END)
            OrdOrigineEntry.insert(0,'')

            self.canvas.draw()
            self.plot(self.canvas, self.ax)

        frameParam = tk.Frame(self.racine, bd=0, bg = '#222831')
        frameParam.pack(side=tk.TOP, fill='x', expand=True)

        frameGauche = tk.Frame(frameParam, bd=0, bg = '#222831')
        frameGauche.pack(side=tk.LEFT, fill='x', expand=True)

        frameDroite = tk.Frame(frameParam, bd=0, bg = '#222831')
        frameDroite.pack(side=tk.RIGHT, fill='x', expand=True)

        OrdOrigineFrame = tk.Frame(frameGauche, bd=0, bg = '#222831')
        OrdOrigineFrame.pack(side=tk.TOP)

        OrdOrigineLabel = tk.Label(OrdOrigineFrame, text="Ord. origine (x10000):", font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE')
        OrdOrigineLabel.grid(row=0, column=0)

        OrdOrigineEntry = tk.Entry(OrdOrigineFrame, bd=0 ,font="Lucida 11 bold", bg = '#EEEEEE', fg= '#222831')
        OrdOrigineEntry.grid(row=0, column=1)

        OrdOrigineValidateButton = tk.Button(OrdOrigineFrame, bd=0, cursor="hand2", text = "Valider", font="Lucida 11 bold", bg = '#393E46', fg= '#EEEEEE', command=setOrdOrigine)
        OrdOrigineValidateButton.grid(row=0, column=2)

        # create scrolled text for the number of the joueurs
        OrdOrigineScale = tk.Scale(frameGauche, from_=-10000, to=10000, orient='horizontal', font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE', relief='flat', highlightthickness=0, troughcolor='#393E46', command= setOrdOrigine)
        OrdOrigineScale.set(self.OrdOrigine*10000)
        OrdOrigineScale.pack(side=tk.TOP, padx=20, fill='x')

        def setDebutTrou(*event):   
            
            self.displayGrain.set(0)
            try:
                if debutTrouEntry.get() != '':
                    debutTrouScale.set(float(debutTrouEntry.get())*10000)
                self.debutTrou = debutTrouScale.get()/10000
            except Exception as e:
                print(f"Valeur de Debut trou dir non valide : {e}")
            debutTrouEntry.delete(0,tk.END)
            debutTrouEntry.insert(0,'')

            self.canvas.draw()
            self.plot(self.canvas, self.ax)   
        
        debutTrouFrame = tk.Frame(frameGauche, bd=0, bg = '#222831')
        debutTrouFrame.pack(side=tk.TOP, pady=(10,0))

        debutTrouLabel = tk.Label(debutTrouFrame, text="Debut Trou (x10000):", font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE')
        debutTrouLabel.grid(row=0, column=0)

        debutTrouEntry = tk.Entry(debutTrouFrame, bd=0 ,font="Lucida 11 bold", bg = '#EEEEEE', fg= '#222831')
        debutTrouEntry.grid(row=0, column=1)

        debutTrouValidateButton = tk.Button(debutTrouFrame, bd=0, cursor="hand2", text = "Valider", font="Lucida 11 bold", bg = '#393E46', fg= '#EEEEEE', command=setDebutTrou)
        debutTrouValidateButton.grid(row=0, column=2)

        debutTrouScale = tk.Scale(frameGauche, from_=0, to=10000, orient='horizontal', font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE', relief='flat', highlightthickness=0, troughcolor='#393E46', command=setDebutTrou)
        debutTrouScale.set(self.debutTrou*10000)
        debutTrouScale.pack(side=tk.TOP, padx=20, fill='x')

        def setLargeurBac(*event):   
            
            self.displayGrain.set(0)
            try:
                if largeurBacEntry.get() != '':
                    largeurBacScale.set(float(largeurBacEntry.get())*10000)
                self.largeurBac = largeurBacScale.get()/10000
            except Exception as e:
                print(f"Valeur de Ord Origine dir non valide : {e}")
            largeurBacEntry.delete(0,tk.END)
            largeurBacEntry.insert(0,'')
            self.canvas.draw()
            self.plot(self.canvas, self.ax)   

        largeurBacFrame = tk.Frame(frameGauche, bd=0, bg = '#222831')
        largeurBacFrame.pack(side=tk.TOP, pady=(10,0))

        largeurBacLabel = tk.Label(largeurBacFrame, text="Largeur Bac (x10000):", font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE')
        largeurBacLabel.grid(row=0, column=0)

        largeurBacEntry = tk.Entry(largeurBacFrame, bd=0 ,font="Lucida 11 bold", bg = '#EEEEEE', fg= '#222831')
        largeurBacEntry.grid(row=0, column=1)

        largeurBacValidateButton = tk.Button(largeurBacFrame, bd=0, cursor="hand2", text = "Valider", font="Lucida 11 bold", bg = '#393E46', fg= '#EEEEEE', command=setLargeurBac)
        largeurBacValidateButton.grid(row=0, column=2)

        largeurBacScale = tk.Scale(frameGauche, from_=0, to=20000, orient='horizontal', font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE', relief='flat', highlightthickness=0, troughcolor='#393E46', command=setLargeurBac)
        largeurBacScale.set(self.largeurBac*10000)
        largeurBacScale.pack(side=tk.TOP, padx=20, fill='x')

        
        def setHauteurBac(*event):  
            
            self.displayGrain.set(0)
            try:
                if hauteurBacEntry.get() != '':
                    hauteurBacScale.set(float(hauteurBacEntry.get())*10000)
                self.hauteurBac = hauteurBacScale.get()/10000
            except Exception as e:
                print(f"Valeur de Ord Origine dir non valide : {e}")
            hauteurBacEntry.delete(0,tk.END)
            hauteurBacEntry.insert(0,'')

            self.canvas.draw()
            self.plot(self.canvas, self.ax)  
        
        hauteurBacFrame = tk.Frame(frameDroite, bd=0, bg = '#222831')
        hauteurBacFrame.pack(side=tk.TOP)

        hauteurBacLabel = tk.Label(hauteurBacFrame, text="Hauteur Bac (x10000):", font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE')
        hauteurBacLabel.grid(row=0, column=0)

        hauteurBacEntry = tk.Entry(hauteurBacFrame, bd=0 ,font="Lucida 11 bold", bg = '#EEEEEE', fg= '#222831')
        hauteurBacEntry.grid(row=0, column=1)

        hauteurBacValidateButton = tk.Button(hauteurBacFrame, bd=0, cursor="hand2", text = "Valider", font="Lucida 11 bold", bg = '#393E46', fg= '#EEEEEE', command=setHauteurBac)
        hauteurBacValidateButton.grid(row=0, column=2)

        hauteurBacScale = tk.Scale(frameDroite, from_=-5000, to=10000, orient='horizontal', font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE', relief='flat', highlightthickness=0, troughcolor='#393E46', command=setHauteurBac)
        hauteurBacScale.set(self.hauteurBac*10000)
        hauteurBacScale.pack(side=tk.TOP, padx=20, fill='x')

        def setNbGrains(*event):

            self.displayGrain.set(0)
            try:
                if nbGrainsEntry.get() != '':
                    nbGrainsScale.set(float(nbGrainsEntry.get()))
                self.nbGrains = nbGrainsScale.get()
            except Exception as e:
                print(f"Valeur de Ord Origine dir non valide : {e}")
            nbGrainsEntry.delete(0,tk.END)
            nbGrainsEntry.insert(0,'')

            self.canvas.draw()
            self.plot(self.canvas, self.ax)
        
        nbGrainsFrame = tk.Frame(frameDroite, bd=0, bg = '#222831')
        nbGrainsFrame.pack(side=tk.TOP, pady=(10,0))

        nbGrainsLabel = tk.Label(nbGrainsFrame, text="Nombre de grains:", font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE')
        nbGrainsLabel.grid(row=0, column=0)

        nbGrainsEntry = tk.Entry(nbGrainsFrame, bd=0 ,font="Lucida 11 bold", bg = '#EEEEEE', fg= '#222831')
        nbGrainsEntry.grid(row=0, column=1)

        nbGrainsValidateButton = tk.Button(nbGrainsFrame, bd=0, cursor="hand2", text = "Valider", font="Lucida 11 bold", bg = '#393E46', fg= '#EEEEEE', command=setNbGrains)
        nbGrainsValidateButton.grid(row=0, column=2)

        nbGrainsScale = tk.Scale(frameDroite, from_=0, to=1000, orient='horizontal', font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE', relief='flat', highlightthickness=0, troughcolor='#393E46', command=setNbGrains)
        nbGrainsScale.set(self.nbGrains)
        nbGrainsScale.pack(side=tk.TOP, padx=20, fill='x')
        
        def setHauteurGrain(*event):

            self.displayGrain.set(0)
            try:
                if hauteurGrainEntry.get() != '':
                    hauteurGrainScale.set(float(hauteurGrainEntry.get())*10000)
                self.hauteur = hauteurGrainScale.get()/10000
            except Exception as e:
                print(f"Valeur de Ord Origine dir non valide : {e}")
            hauteurGrainEntry.delete(0,tk.END)
            hauteurGrainEntry.insert(0,'')

            self.canvas.draw()
            self.plot(self.canvas, self.ax)
        
        hauteurGrainFrame = tk.Frame(frameDroite, bd=0, bg = '#222831')
        hauteurGrainFrame.pack(side=tk.TOP, pady=(10,0))

        hauteurGrainLabel = tk.Label(hauteurGrainFrame, text="Hauteur Grain (x10000):", font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE')
        hauteurGrainLabel.grid(row=0, column=0)

        hauteurGrainEntry = tk.Entry(hauteurGrainFrame, bd=0 ,font="Lucida 11 bold", bg = '#EEEEEE', fg= '#222831')
        hauteurGrainEntry.grid(row=0, column=1)

        hauteurGrainValidateButton = tk.Button(hauteurGrainFrame, bd=0, cursor="hand2", text = "Valider", font="Lucida 11 bold", bg = '#393E46', fg= '#EEEEEE', command=setHauteurGrain)
        hauteurGrainValidateButton.grid(row=0, column=2)

        hauteurGrainScale = tk.Scale(frameDroite, from_=0, to=20000, orient='horizontal', font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE', relief='flat', highlightthickness=0, troughcolor='#393E46', command=setHauteurGrain)
        hauteurGrainScale.set(self.hauteur*10000)
        hauteurGrainScale.pack(side=tk.TOP, padx=20, fill='x')

        

        
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
        x_debutTrou_gauche = (self.debutTrou - self.OrdOrigine)/self.CoeffDir
        x_debutTrou_droite = (self.debutTrou - self.OrdOrigine)/self.CoeffDir
        X1 = np.linspace(self.largeur_silo_gauche, x_debutTrou_gauche, 100000)
        X2 = np.linspace(x_debutTrou_droite, self.largeur_silo_droite, 100000)
        plt.plot(X1, self.paroiGauche(X1), color='#EEEEEE')
        plt.plot(X2, self.paroiDroite(X2), color='#EEEEEE')
        X3 = np.linspace(-self.largeurBac/2, self.largeurBac/2, 100000)
        Y3 = np.zeros(100000) + self.hauteurBac
        plt.plot(X3, Y3, color='#EEEEEE')
        plt.xlim([self.limite_gauche, self.limite_droite])
        plt.ylim([self.limite_bas, self.limite_haut])
        plt.grid()
        plt.tight_layout()                                          # On supprime les marges de la figure

        self.canvas=FigureCanvasTkAgg(self.fig, master=self.racine)

        displayGrainCheckBox = tk.Checkbutton(self.racine, onvalue=1, offvalue=0, text="Afficher les grains", font="Lucida 11 bold", bg = '#222831', fg= '#EEEEEE', selectcolor="#222831",  bd = 0, activebackground="#393E46", activeforeground="#EEEEEE", variable=self.displayGrain, command=lambda:self.plot(self.canvas, self.ax))
        displayGrainCheckBox.pack(side=tk.TOP)

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill='x')
        self.canvas.draw()


        validateButton = tk.Button(self.racine, text="Enregistrer", bg = '#D65A31', fg= '#EEEEEE', bd=0, font ='Lucida 16 bold', command=self.save)
        self.racine.bind("<Return>", self.save)
        validateButton.pack(side=tk.BOTTOM, fill='x')

app = App()
app.racine.mainloop()
