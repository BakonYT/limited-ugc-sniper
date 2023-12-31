# Imports here
from themes.required.visual import Visual
from themes.required.sniper import UGCSniper

# Print class definition
def printLogo():
    '''

    :return: int success
    '''

    Visual.betterPrint(
        '''[GRADIENT_#00C800_#005000]
  SSSSS   HH     HH   AAAAA   PPPPPP   EEEEEE   SSSSS   HH     HH   IIIIII   FFFFFFF   TTTTTTT  EEEEEE   RRRRRR    
 S        HH     HH  AA    AA  PP   PP  EE      S       HH     HH     II     FF        TT     EE       RR   RR   
  SSSSS   HHHHHHHHH  AAAAAAAAA  PPPPPP   EEEEEE   SSSSS   HHHHHHHHH     II     FFFFF     TT     EEEEEE   RRRRRR    
      SS  HH     HH  AA    AA  PP       EE           SS  HH     HH     II     FF        TT     EE       RR  RR    
 SSSSS    HH     HH  AA    AA  PP       EEEEEE   SSSSS   HH     HH   IIIIII   FF        TT     EEEEEE   RR   RR   

 SSSSS   NN    NN IIIIII PPPPPP  EEEEEE  RRRRR   
SS      NNN   NN   II   PP   PP EE      RR   RR  
 SSSSS  NN N  NN   II   PPPPPP  EEEEEE  RRRRR   
     SS NN  NNN    II   PP      EE      RR  RR   
 SSSSS  NN   NN IIIIII PP      EEEEEE  RR   RR  
[END]'''
    )
    return 1

def printText(sniper: UGCSniper, logs):
    '''
    :param: sniper: the sniper with all variables
    :param: logs: The logs made by the sniper will automatically reset after 3 iterations

    :return: bool success
    '''

    Visual.betterPrint(f"""    [COLOR_WHITE][Time: [COLOR_YELLOW][{sniper._time}][COLOR_WHITE]]
        [COLOR_WHITE]--> [Speed: [COLOR_YELLOW]{sniper.speed}[COLOR_WHITE]]
        [COLOR_WHITE]--> [Ratelimits: [COLOR_RED]{sniper.ratelimits}[COLOR_WHITE]]

    [COLOR_WHITE][Price checks made: [COLOR_GREEN]{sniper.checks_made}[COLOR_WHITE]]
    [COLOR_WHITE][Limiteds added: [COLOR_GREEN]{len(sniper.limiteds)}[COLOR_WHITE]]
    [COLOR_GREEN][UGC Items bought][COLOR_WHITE]
        --> [COLOR_WHITE][Bought UGCs: [COLOR_GREEN]{sniper.bought}[COLOR_WHITE]]
        --> [COLOR_WHITE][Bought paid UGCs: [COLOR_GREEN]{sniper.boughtpaid}[COLOR_WHITE]]
    [COLOR_WHITE][Changed Proxies: [COLOR_RED]{sniper.proxies_switched}[COLOR_WHITE]]
        [COLOR_WHITE]--> [Current Proxy: [COLOR_YELLOW]{sniper.proxy}[COLOR_WHITE]]
    [COLOR_WHITE][Status: [COLOR_YELLOW]{sniper.proxy}[COLOR_WHITE]]
    
    Logs:
{logs}
    """)

    return 1

