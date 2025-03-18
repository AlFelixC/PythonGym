from PerceptionConstants import *

def AttackModule(self, perception):
    priority = {
        COMMAND_CENTER:0,
        SHELL: 1,   # Prioridad más alta
        PLAYER: 2,
        BRICK: 3,
        UNBREAKABLE: 4,
        NOTHING: 5,
        OTHER:6
    }
    print("ATACANDO AL OBJETIVO")

    #Almacenaremos el objetivo prioritario
    mainTarget = None
    dirTarget = None
    
    #Modo busqueda para escoger el objetivo mas prioritario
    for i, direction in enumerate(dirs):
        #Encuentra el tipo
        targetType = perception[direction]

        #Y comprueba cual tiene mayor prioridad
        if targetType != NOTHING and targetType != UNBREAKABLE and targetType != OTHER:
            if mainTarget is None or priority[targetType] < priority[mainTarget]:
                mainTarget = targetType
                dirTarget = i

    #Dispara al objetivo en su direccion
    if mainTarget is not None:
        self.state = EXPLORE  
        return movingDirs[dirTarget], True
    
    #Si no hay objetivos vuelve a explorar
    self.state = EXPLORE
    return STAY, True
