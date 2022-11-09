# TODO make logger object/methods that will recieve information and, depending on importance,
#   show it to the user and log it in a file or just log it to a file
import datetime
import logging
import os

from rich.logging import RichHandler


def log(console, severity, message):
    
    # Init required values

    if not os.path.exists('.logs'):
        os.makedirs('.logs')

    _time = datetime.date.today()
    FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
    logging.basicConfig(filename='.logs/{}.log'.format(_time), format=FORMAT, level=logging.INFO, datefmt="[%X]")
    log = logging.getLogger("rich")
    # log.addHandler(RichHandler())

    if severity == 'info':
        print_info(log, message)
    elif severity == 'warn':
        print_warn(log, console, message)
    elif severity == 'err':
        print_err(log, console, message)


def print_info(log, message):
    log.info(message)
    return

def print_warn(log, console, message):
    log.warning(message)
    console.log(f'[bold orange] [WARN] {message}')

def print_err(log, console, message):
    log.warning(message)
    console.log(f'[bold red] [ERR] {message}')
     

