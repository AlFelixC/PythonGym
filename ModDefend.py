from PerceptionConstants import *


#Logica para la defensa. Dispararemos a los misiles
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

    #Que esquive el misil si tiene tiempo y espacio disponible
    if defense == True and perception[dist[dirShell]] > 8:
        for orientation in dirsHuida:
            if dirShell != orientation:
                print("DODGING THE SHELL")
                self.state = EXPLORE
                return orientation, False

    #No nos moveremos hacia donde esta la bala
    if defense == True: #1
        for orientacion in dirsHuida:
            if dirShell != orientacion:
                self.state = ATTACK
                return orientacion, False #Cambio a False estaba en true

    #Nos orientamos y abrimos fuego
    if dirShell != -1:
        print("SHOOTING TOWARDS THE SHELL")
        self.state = ATTACK
        return dirShell, False #Cambio a False estaba en true

    self.state = EXPLORE
    return STAY, False
