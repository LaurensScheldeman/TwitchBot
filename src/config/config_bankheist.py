
from src.config.config_pointsystem import pointsystem_config

bankheist_config = {

    'enable_bankheist': True, # Global setting to enable/disable bankheist minigame

    ###############################
    # SECTION 1 : ENTERY OF HEIST #
    ###############################
    'activation_command': '!bankheist',
    'activation_command_usage': '!bankheist [bet] (full integer)',

    'max_bet': 5000, # Set to zero for unlimited
    'currency_name': pointsystem_config['currency_name'],
    'time_to_enter': 120, # Time (in seconds) between first entery and start of the heist

    # These messages will be visible together with the entery_message_1 (see further below)
    'entery_instructions': 'Type @activation_command@ [x] to enter.',
    'max_entery_message': 'Buy-in top\'s out at @max_bet@ @currency_name@.',

    # When a heist is already in progress, entering denied
    'late_entery': 'Sorry @user@, you are too late. The crew is in the middle of a heist. Come back for the next one.',

    ###############################
    # SECTION 2: HEIST LEVELS     #
    ###############################

    # Custom names for the banks
    'level_1_bank_name': 'ShredNation Municipal Bank',
    'level_2_bank_name': 'ShredNation City Bank',
    'level_3_bank_name': 'ShredNation State Bank',
    'level_4_bank_name': 'ShredNation National Reserve',
    'level_5_bank_name': 'ShredNation Federal Reserve',

    # Make sure each level has a greater max user limit than the level before
    # level 1 must have at least 1 as max user
    'level_1_max_users': 1,
    'level_2_max_users': 2,
    'level_3_max_users': 5,
    'level_4_max_users': 10,

    # Next level heist message
    'entery_message_1': '@user@ has started planning a bank heist! Looking for a bigger crew for a bigger score. Join in!',
    'entery_message_2': 'With this crew, we can now hit the @level_2_bank_name@. Lets see if we can get a bigger crew to hit the @level_3_bank_name@!',
    'entery_message_3': 'Oh yeah! With this crew, we can now hit the @level_3_bank_name@. Lets see if we can get a bigger crew to hit the @level_4_bank_name@!',
    'entery_message_4': 'Hell yeah! We can now hit the @level_4_bank_name@. A few more, and we could hit the @level_5_bank_name@!',
    'entery_message_5': 'Epic crew! We are going to hit the @level_5_bank_name@ guys! Gear up and get ready to head out.',

    ###############################
    # SECTION 3: GAME OUTCOMES    #
    ###############################

    'heist_start': 'Alright guys, check your guns. We are storming into the @bankname@ through all entrances. Let\'s get the cash and get out before the cops get here.',

    # Single user heist
    'single_succes': '@user@ executed the heist flawlessly, sneaking into the @bankname@ through the back entrance and looting @totalwinamount@ @currency_name@ from the vault.',
    'single_fail': 'Local security caught @user@ trying to sneak into the @bankname@ through the back entrance and opened fire.',

    # Multi user heist
    'multi_succes_100%': 'The execution was flawless, in and out before the first cop arrived on scene. The whole crew got away scoring @totalwinamount@ @currency_name@ from the vault.',
    'multi_succes_34-99%': 'The crew suffered a few losses engaging the local security team. The remaining crew got away scoring @totalwinamount@ @currency_name@ from the vault before backup arrived.',
    'multi_succes_1-33%': 'The crew suffered major losses as they engaged the SWAT backup. The remaining crew barely made it scoring @totalwinamount@ @currency_name@ from the vault.',
    'multi_fail': 'SWAT teams nearby stormed the bank and killed the entire crew. Not a single soul survived...',

    'heist_outcome': 'The heist payouts are:',

    ###############################
    # SECTION 4: PAYOUT RATES     #
    ###############################

    # Changes to win (measured in %)
    'level_1_win': 54,
    'level_2_win': 48.8,
    'level_3_win': 42.5,
    'level_4_win': 38.7,
    'level_5_win': 32.4,

    # Payout ratios
    'level_1_win_multiplier': 2,
    'level_2_win_multiplier': 3,
    'level_3_win_multiplier': 4,
    'level_4_win_multiplier': 5,
    'level_5_win_multiplier': 6,


    ###############################
    # SECTION 4 : COOLDOWN TIMER  #
    ###############################
    'cooldown_time': 15, # Time between game outcome and start of next game entery in minutes
    'cooldown_message': 'The cops are on high alert afther last job, we have to lay low for a bit. Call me again afther @cooldown_time_left@ minutes.',
    'cooldown_over_message': 'Looks like the cops have given up the search ... the banks are ripe for hittig!'

} # End of bankheist_config
