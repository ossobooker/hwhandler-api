import logging

class SystemConfigError(Exception):
    pass

def validate_system(config):
    """Get system definition (config) and validate it.

    Requirements:
    - Each ID should be unique.
    - Each Board should have a valid shelf.
    - Same for data-clock_managers."""
   
    # check if each ID is unique
    validate_ids(config)

    # chekc if each board/dcm has a valid shelf
    validade_hardware_shelf(config)

def validade_hardware_shelf(config):
    """Checker whether each board/dcm has a valid shelf."""
    shelf_ids = [ shelf['id'] for shelf in config["system"]["shelves"] ]

    # boards
    for board in config["system"]["boards"]:
        if not(board['shelf'] in shelf_ids):
            message = f"Board {board['id']} is set to a unidentified shelf. Check your system config yaml."
            logging.error(message)
            raise SystemConfigError(message)
    
    # data-clock-managers
    for dcm in config["system"]["data-clock-managers"]:
        # print(shelf_ids)
        # print(dcm['shelf'])
        if not(dcm['shelf'] in shelf_ids):
            message = f"Data-clock-manager {dcm['id']} is set to a unidentified shelf. Check your system config yaml."
            logging.error(message)
            raise SystemConfigError(message)


def validate_ids(config):
    """Check if each ID in the configuration dict is unique."""

    system_ids = []
    system_ids += [ board['id'] for board in config["system"]["boards"] ]
    system_ids += [ shelf['id'] for shelf in config["system"]["shelves"] ]
    system_ids += [ dcm['id'] for dcm in config["system"]["data-clock-managers"] ]

    if len(system_ids) != len(set(system_ids)):
        message = f"There is a non-unique component ID. Check your system config yaml."
        logging.error(message)
        raise SystemConfigError(message)