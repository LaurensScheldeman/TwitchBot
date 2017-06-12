
pointsystem_config = {

    'currency_name': 'Shreckles',

    # Number of points added when a user watch for an hour.
    # Adding interval depends on config_userdata -> update_rate.
    'points_over_time': 1000000,

    # Check balance
    'check_balance_command': '!shreckles',
    'check_balance_cooldown': 2,
    'check_balance_message': 'You have currently @amount@ @currency_name@.',

    # Transfering points to an other user
    'transfer_command': '!give',
    'transfer_command_usage': '!give [user] [amount]'

} # end of currencySystem_config
