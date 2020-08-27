import logging
from hwhandler_api.core import BaseCommand

class dummy(BaseCommand): 
  def pre_command(self):
      logging.info(f'Preparing a dummy command...') 
      return 0

  def exec_command(self):
      logging.info(f'Executing a dummy command...') 
      return 0

  def post_command(self):
      logging.info(f'Post-processing a dummy command...')
      return 0

