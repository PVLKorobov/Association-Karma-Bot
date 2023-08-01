from tools import config_handler

from string import punctuation


config = config_handler.parse_config()


def get_score_name(scoreAmount: int) -> str:
    if scoreAmount in range(5, 20) or scoreAmount == 0:
        return config['scoreNames']['high']
    else:
        scoreAmount %= 10
        if scoreAmount == 1:
            return config['scoreNames']['low']
        if (scoreAmount == 0) or (5 <= scoreAmount):
            return config['scoreNames']['high']
        else:
            return config['scoreNames']['mid']
    

def get_param_state(paramValue: bool) -> str:
    if paramValue:
        return 'включен'
    else:
        return 'отключен'
    

def has_punctiation_marks(input: str) -> bool:
    for symbol in input[1:]:
        if symbol in punctuation:
            return True
    return False
    

def get_command_argument(inputText: str, dividerCount: int = 1, numeric: bool = True) -> list:
    divider = ' '
    if inputText.count(divider) != dividerCount or has_punctiation_marks(inputText):
        raise Exception
    else:
        args = inputText.split(divider)[1:]
        if numeric:
            for arg in args:
                if not arg.isnumeric():
                    raise Exception
        return args
    
