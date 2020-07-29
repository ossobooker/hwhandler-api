class BaseCommand():
    def __init__(self):
        self.pre_command()
        self.exec_command()
        self.post_command()

    def pre_command(self):
        return 0

    def exec_command(self):
        return 0

    def post_command(self):
        return 0
      
if __name__ == '__main__':
    cmd = BaseCommand()

