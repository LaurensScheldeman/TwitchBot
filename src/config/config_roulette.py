
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

    'entery_start_message': '@user@ started a new roulette round, place your bet to play: !roulette [bet] [option].',
    'max_entery_message': 'Bets are limited to @max_bet@ @currency_name@.',
    'entery_help_message': 'For more information, type !roulette help.',

    # When betting is closed, entering denied
    'late_entery': 'Sorry @user@, betting is closed for this round, come back for the next one.'

} # End of roulette_config
