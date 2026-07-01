# parser.py 
def parse_line(tokens):
    if not tokens:
        return None 
    first = tokens[0]
# fire/flood/ forest_fire at <district> severity <number>
    if first == ("KEYWORD", "FIRE") or first == ("KEYWORD", "FLOOD") or first == ("KEYWORD","FOREST_FIRE"):
        if len(tokens) != 5:
            raise SyntaxError(f"Invalid incident command: {tokens}")
        if tokens[1] != ("KEYWORD", "AT"):
            raise SyntaxError(f"Expected 'AT' after incident type: {tokens}")
        if tokens[3] != ("KEYWORD", "SEVERITY"):
            raise SyntaxError(f"Expected SEVERITY, got {tokens[3]}")
        if tokens[4][0] != "NUMBER":
            raise SyntaxError(f"Expected number for severity, got {tokens[4]}")
        return {
            "type": "INCIDENT",
            "disaster": first[1],
            "district": tokens[2][1],
            "severity": tokens[4][1]
        }
    #allocate <number> <resource TO <district>
    if first == ("KEYWORD", "ALLOCATE"):
        if len(tokens) != 5:
            raise SyntaxError(f"Invalid ALLOCATE command: {tokens}")
        if tokens[1][0] != "NUMBER":
            raise SyntaxError(f"Expected number after ALLOCATE, got {tokens[1]}")
        if tokens[3] != ("KEYWORD", "TO"):
            raise SyntaxError(f"Expected TO, got {tokens[3]}")
        return {
        "type": "ALLOCATE",
        "quantity": tokens[1][1],
        "resource": tokens[2][1],
        "district": tokens[4][1]
        }
# If severity > <number> THEN dispatch <team>
    if first == ("KEYWORD", "IF"):
        if len(tokens) != 7:
            raise SyntaxError(f"Invalid IF command: {tokens}")
        if tokens[2] != ("OPERATOR", ">"):
            raise SyntaxError(f"Expected >, got {tokens[2]}")
        if tokens[3][0] != "NUMBER":
            raise SyntaxError(f"Expected number, got {tokens[3]}")
        if tokens[4] != ("KEYWORD", "THEN"):
            raise SyntaxError(f"Expected THEN, got {tokens[4]}")
        if tokens[5] != ("KEYWORD", "DISPATCH"):
            raise SyntaxError(f"Expected DISPATCH, got {tokens[5]}")
        return {
            "type": "DISPATCH_RULE",
            "threshold": tokens[3][1],
            "team": tokens[6][1]
        }

    # ROAD <district> <district> blocked/open
    if first == ("KEYWORD", "ROAD"):
        if len(tokens) != 4:
            raise SyntaxError(f"Invalid ROAD command: {tokens}")
        if tokens[3] not in [("KEYWORD", "BLOCKED"), ("KEYWORD", "OPEN")]:
            raise SyntaxError(f"Expected BLOCKED or OPEN, got {tokens[3]}")
        return {
            "type": "ROAD_UPDATE",
            "from_district": tokens[1][1],
            "to_district": tokens[2][1],
            "status": tokens[3][1].lower()
        }

    # WHEN <condition_var> > <number> SEND <message> TO <target>
    if first == ("KEYWORD", "WHEN"):
        if len(tokens) != 8:
            raise SyntaxError(f"Invalid WHEN command: {tokens}")
        if tokens[2] != ("OPERATOR", ">"):
            raise SyntaxError(f"Expected >, got {tokens[2]}")
        if tokens[3][0] != "NUMBER":
            raise SyntaxError(f"Expected number, got {tokens[3]}")
        if tokens[4] != ("KEYWORD", "SEND"):
            raise SyntaxError(f"Expected SEND, got {tokens[4]}")
        if tokens[6] != ("KEYWORD", "TO"):
            raise SyntaxError(f"Expected TO, got {tokens[6]}")
        return {
            "type": "ALERT",
            "condition_var": tokens[1][1],
            "threshold": tokens[3][1],
            "message": tokens[5][1],
            "target": tokens[7][1]
        }

    raise SyntaxError(f"Unknown command starting with: {first}")


def parse(token_lines):
    ast = []
    for tokens in token_lines:
        node = parse_line(tokens)
        if node:s
            ast.append(node)
    return ast


# Test
if __name__ == "__main__":
    from lexer import lex

    script = """
FIRE at Kailali severity 8
FLOOD at Bardiya severity 6
ALLOCATE 3 firetrucks TO Bardiya
IF severity > 7 THEN dispatch helicopter_team
ROAD Dang Surkhet blocked
WHEN wind_speed > 40 SEND warning TO all_districts
"""
    token_lines = lex(script)
    ast = parse(token_lines)
    for node in ast:
        print(node)