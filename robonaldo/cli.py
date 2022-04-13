from robonaldo.command import CommandManager
from robonaldo.core import Robonaldo


class Prompt:
    def __init__(self):
        CommandManager().register_all()

    def run(self) -> None:
        success = None
        while True:
            prefix = ''
            if success is not None:
                if success:
                    prefix = '[✓] '
                else:
                    prefix = '[✗] '

            command = input(prefix + "Enter a command [help] > ").strip()
            if len(command) > 0:
                result, message = CommandManager().handle(command)
                if not result:
                    print(message)
                
                success = result
            
if __name__ == "__main__":
    Prompt().run()