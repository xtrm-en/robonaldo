class ExampleTrackingStrategy(RobotStrategy):
    # Definir le nom de la strategie (utile pour la communication inter-strat)
    def __init__(self):
        super().__init__("tracking")

    # Qu'est ce que les robots doivent faire durant cette strategie
    def update(self, ctx: GameContext, robot: Robot):
        robot.spin()

    # Activer cette strategie si la balle se retrouve dans notre quart de terrain
    def is_active(self, ctx: GameContext) -> bool:
        return ctx.terrain.get_relative_pos(ctx.ball) < 0.25

    # Ne pas accepter cette strategie si la defense doit aussi s'executer
    def should_override(self, ctx: GameContext, strategies: list) -> bool:
        return not strategies.__contains__('defense')
