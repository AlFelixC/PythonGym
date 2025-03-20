from PerceptionConstants import *


#Logica de defenderse siempre vamos disparar al misil
def DefendModule(self, perception):
    defense = False
    dirShell = -1
    dirsHuida = []

    #Obtenemos la direccion del misil y direcciones donde haya hueco
    for actDir, moves in enumerate(dirs):
        if perception[moves] == SHELL:
            dirShell = actDir
            defense = True
            print("MISIL DETECTADO")
        elif perception[moves] == NOTHING:
            dirsHuida.append(actDir)  #Guardamos esas posiciones con hueco para poder huir

    #No nos moveremos hacia donde esta la bala
    if defense == True: #1
        for orientacion in dirsHuida:
            if dirShell != orientacion:
                self.state = ATTACK
                return orientacion, True

    #Nos orientamos y abrimos fuego
    if dirShell != -1:
        print("SHOOTING TOWARDS THE SHELL")
        self.state = ATTACK
        return dirShell, True

    self.state = EXPLORE
    return STAY, False
