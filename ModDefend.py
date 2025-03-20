from PerceptionConstants import *


#Logica de defenderse siempre vamos disparar al misil
def DefendModule(self, perception):
    defense = False #0
    dirShell = -1
    emptyDirs = []

    #Obtenemos la direccion del misil y direcciones donde haya hueco
    for actDir, moves in enumerate(dirs):
        if perception[moves] == SHELL:
            dirShell = actDir
            self.state = DEFEND
            defense = True #1
            print("MISIL DETECTADO")
        elif perception[moves] == NOTHING:
            emptyDirs.append(actDir)  #Guardamos esas posiciones con hueco

    print("Valor de dirShell: ", dirShell)
    #No nos moveremos hacia donde esta la bala
    if defense == True: #1
        for orientacion in emptyDirs:
            if dirShell != orientacion:
                return orientacion, True

    #Nos orientamos y abrimos fuego
    if dirShell != -1:
        print("SHOOTING TOWARDS THE SHELL")
        self.state = ATTACK
        return dirShell, True

    self.state = EXPLORE
    return STAY, False
