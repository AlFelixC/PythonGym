from PerceptionConstants import *


#Logica para la defensa. Dispararemos a los misiles
def DefendModule(self, perception):
    defense = False
    shoot = False
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
    if defense == True and perception[dist[dirShell]] > 9:
        for orientation in dirsHuida:
            if dirShell == orientation:
                print("DODGING THE SHELL")
                self.state = EXPLORE
                return orientation, shoot

    #Disparamos hacia el misil
    if defense == True:
        for orientacion in dirsHuida:
            if dirShell != orientacion:
                print("SHOOTING TOWARDS THE SHELL")
                shoot = True
                return orientacion, shoot

    #Nos orientamos y abrimos fuego
    if dirShell != -1:
        print("TURNING TO SHOOT")
        shoot = True
        return dirShell, shoot

    self.state = EXPLORE
    return STAY, shoot
