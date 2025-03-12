from PerceptionConstants import *


#Logica de defenderse, aqui no huimos JAMAS, si te tiran una bala te posicionas y la disparas, una vez eliminada, vuelves al estado de wandering
def DefendModule(self, perception):
    defensa = 0
    dirShell = -1
    emptyDirs = []

    #Obtenemos la direccion del misil y direcciones donde haya hueco
    for i, moves in enumerate(dirs):
        if perception[moves] == SHELL:
            dirShell = i
            self.state = DEFEND
            defensa = 1
            print("MISIL DETECTADO")
        elif perception[moves] == NOTHING:
            emptyDirs.append(i)  #Guardamos esas posiciones con hueco

    # Si encontramos una bala y hay direcciones vacías, evitamos movernos hacia la bala
    if defensa == 1:
        # Intentamos movernos a una dirección vacía que no sea la dirección de la bala
        for orientacion in emptyDirs:
            if orientacion != dirShell:
                return orientacion, False  # Moverse a la dirección donde hay hueco

    # Si no hay direcciones vacías o todas las direcciones están hacia la bala
    # Giramos hacia la dirección de la bala y disparamos
    if dirShell != -1:
        print("No hay escapatoria, girando hacia la bala y disparando")
        self.state = ATTACK  # Cambiar el estado a ATTACKING
        return dirShell, True  # Girar hacia la bala y disparar (1 para disparar)

    # Si no hay dirección vacía ni dirección de bala, permanecemos en STAY
    self.state = DEFEND
    return STAY, False  # Se queda en su lugar (no hace nada)
