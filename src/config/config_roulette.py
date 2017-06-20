
from src.config.config_pointsystem import pointsystem_config

roulette_config = {

    'enable_roulette': True,

    ###############################
    # SECTION 1 : ENTERY OF ROUND #
    ###############################

    # !roulette help
    'usage_help': '!roulette [bet] [option]',

    'activation_command': '!roulette',
    'activation_command_usage': '!roulette [bet] [option] (For more info: !roulette help',

    'max_bet': 500,
    'currency_name': pointsystem_config['currency_name'],
    'time_to_enter': 300, # Time (in seconds) between first entery and start of the heist

    # When betting is closed, entering denied
    'late_entery': 'Sorry @user@, betting is closed for this round, come back for the next one.',



    'outcome': 'The winning number was @number@.',
    'result_winning': 'Roulette winners are:'

} # End of roulette_config
