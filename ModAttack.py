from PerceptionConstants import *

def AttackModule(self, perception):
    #Le vamos a asignar unos valores de prioridad por si hay varios objetivos a disposicion
    #para que elija el que nosotros queremos en orden
    #Almacenaremos el objetivo prioritario
    mainTarget = -1
    dirTarget = -1
    futureDir = STAY
    shoot = False

    priority = {
        SHELL: 0, #Mantenerse vivo es su prioridad antes que seguir con el objetivo
        COMMAND_CENTER: 1, PLAYER: 2, BRICK: 3
    }
    print("ENTERING ATTACK MODE >:(")
    
    #Modo busqueda para escoger el objetivo mas prioritario
    #Lo transformamos el valor en "i" porque no nos permite devolver una tupla
    for i, direction in enumerate(dirs):
        #Obtenemos el tipo de lo que tenemos a disposicion
        targetType = perception[direction]

        #Comprobamos cual es nuestra prioridad
        if targetType != NOTHING and targetType != UNBREAKABLE and targetType != OTHER:
            if mainTarget == -1 or priority[targetType] < priority[mainTarget]:
                mainTarget = targetType
                dirTarget = i

    #Dispara al objetivo en su direccion
    if mainTarget != -1:
        futureDir = movingDirs[dirTarget]
        shoot = True
    
    #Si no hay objetivos vuelve a explorar
    self.state = EXPLORE
    return futureDir, shoot
