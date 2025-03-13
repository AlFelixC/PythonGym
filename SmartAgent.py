import random
from BaseAgent import BaseAgent
from PerceptionConstants import *
from ModAttack import AttackModule
from ModDefend import DefendModule
from ModExplore import ExploreModule
#SmartAgent.py es un NPC que estamos creando apartir de BaseAgente.py, clase de la cual hereda sus funciones
#y nosotros sobrecargamos estas funciones para que realice sus actividades de manera totalmente autonoma
class SmartAgent(BaseAgent):
  
    def __init__(self, id, name):
        super().__init__(id, name)
        self.state = EXPLORE
        self.map = [[-1 for _ in range(13)] for _ in range(13)]

    def Update(self, perception):
        print(f"SmartAgent 47 en estado: {self.state}")
        print(perception)

        if self.state == EXPLORE:
            return ExploreModule(self, perception)
        elif self.state == ATTACK:
            return AttackModule(self, perception)
        elif self.state == DEFEND:
            return DefendModule(self, perception)


