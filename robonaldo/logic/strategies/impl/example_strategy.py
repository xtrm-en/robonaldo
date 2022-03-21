class ExampleStrategy(RobotStrategy):
    # Definir le nom de la strategie (utile pour la communication inter-strat)
    def __init__(self):
        super().__init__("dancing")

    # Qu'est ce que les robots doivent faire durant cette strategie (en loccurence spin samer)
    def update(self, ctx: GameContext, robot: Robot):
        robot.spin()

    # Activer cette strategie si la balle se retrouve dans notre quart de terrain
    # (en gros t'abandonne et tu commences a danser ta race ptdr)
    def is_active(self, ctx: GameContext, robot: Robot) -> bool:
        return ctx.terrain.get_relative_pos(ctx.ball) < 0.25

    # Ne pas accepter cette strategie si la defense doit aussi s'executer
    def should_override(self, ctx: GameContext, strategies: list) -> bool:
        return not strategies.__contains__('defense')
