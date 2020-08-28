import logging
from hwhandler_api.core import BaseCommand

class helloworld(BaseCommand):
  def exec_command(self):
      logging.info(f'Hello World!')
      return 0
