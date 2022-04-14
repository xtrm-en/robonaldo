from robonaldo.context.game import GameContext
from robonaldo.context.robot import Robot
from robonaldo.context.updater import ContextUpdater
from robonaldo.controller import RobotController
from robonaldo.utils import Singleton

class RobotStrategy:
    def update(self, ctx: GameContext, robot: Robot, controller: RobotController) -> None:
        pass

ctx = None


def execute_attack(attack):
    while True:
        if ctx is not None:
            attack.process(ctx)

def execute_defense(defense):
    while True:
        if ctx is not None:
            defense.process(ctx)


class StrategyManager(metaclass = Singleton):
    __target = "robonaldo/strategies"
    __reg = False

    attack = None
    attack_thread = None
    defense = None
    defense_thread = None

    def construct(self) -> None:
        sys.path.append(self.__target)
        for file in os.listdir(self.__target):
            if '.py' in file and '.pyc' not in file and '__' not in file:
                name = file.replace('.py', '')
                __import__(name)

        self.attack_thread = threading.Thread(target=execute_attack, args=(attack,))
        self.attack_thread.start()
        self.defense_thread = threading.Thread(target=execute_defense, args=(defense,))
        self.defense_thread.start()

    def register_on(self, updater: ContextUpdater) -> None:
        if self.__reg is not True:
            self.__reg = True
            updater.register(lambda ctx, dt: self.__update(ctx, dt))
        else:
            raise Exception("Tried registering StrategyManager twice.")

    def __update(self, _ctx: GameContext, delta_time: float) -> None:
        ctx = _ctx
