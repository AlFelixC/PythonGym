from PerceptionConstants import *


#Logica de defenderse siempre vamos disparar al misil
def DefendModule(self, perception):
    defense = 0
    dirShell = -1
    emptyDirs = []

    #Obtenemos la direccion del misil y direcciones donde haya hueco
    for i, moves in enumerate(dirs):
        if perception[moves] == SHELL:
            dirShell = i
            self.state = DEFEND
            defense = 1
            print("MISIL DETECTADO")
        elif perception[moves] == NOTHING:
            emptyDirs.append(i)  #Guardamos esas posiciones con hueco

    #No nos moveremos hacia donde esta la bala
    if defense == 1:
        for orientacion in emptyDirs:
            if dirShell != orientacion:
                return orientacion, False

    #Nos orientamos y abrimos fuego
    if dirShell != -1:
        print("No hay escapatoria, girando hacia la bala y disparando")
        self.state = ATTACK
        return dirShell, True

    self.state = EXPLORE
    return STAY, False
