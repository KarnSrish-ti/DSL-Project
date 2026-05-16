# lexer.py
KEYWORDS ={
    "FIRE",'FLOOD',"FOREST_FIRE","ALLOCATE",'TO','IF',"THEN","DISPATCH","ROAD","BLOCKED","OPEN","WHEN","SEND","AT","SEVERITY" }
def tokenize(line):
    tokens = []
    words = line.split()
    for word in words:
        if word == ">":
            tokens.append(('OPERATOR', '>'))
        elif word.upper() in KEYWORDS:
            tokens.append(('KEYWORD', word.upper()))
        elif word.isdigit():
            tokens.append(('NUMBER', int(word)))
        else:
            tokens.append(('IDENTIFIER', word))
    return tokens

def lex(scrpit):
    all_tokens = []
    lines = script.strip().split('\n')

    for line in lines:
        line =line.strip()
        if line == "" or line.startswith("#"):
            continue
        tokens = tokenize(line)
        all_tokens.append(tokens)
    return all_tokens

# TEST
if __name__ == "__main__":
    script = """
    # Sample dispatch script 
    FIRE at Kailali severity 8
    FLOOD at Bardiya severity 6
    ALLOCATE 3 firetrucks TO Bardiya 
    IF severity > 7 THEN dispatch helicopter_team
    ROAD Dang Surkhet blocked 
    WHEN wind_speed > 40 SEND warning TO all_districts
    """
    result = lex(script)
    for line_tokens in result:
        print(line_tokens)