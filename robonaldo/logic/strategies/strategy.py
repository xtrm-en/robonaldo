class RobotStrategy:
    def __init__(self, strat_id: str):
        self.__id = strat_id

    def get_id(self) -> str:
        return self.__id

    def update(self, ctx: GameContext, robot: Robot):
        pass

    def activate_on(self, ctx: GameContext) -> Robot:
        return None

    def should_override(self, ctx: GameContext, strategies: list) -> bool:
        return False
