# main.py

from lexer import lex
from parser import parse
from interpreter import execute, print_report

script = """
ROAD Dang Surkhet blocked
FIRE at Kailali severity 8
FLOOD at Bardiya severity 6
FOREST_FIRE at Dang severity 5
ALLOCATE 3 firetrucks TO Kailali
ALLOCATE 2 helicopters TO Bardiya
IF severity > 7 THEN DISPATCH helicopter_team
IF severity > 4 THEN DISPATCH fire_brigade
WHEN wind_speed > 40 SEND warning TO all_districts
WHEN flood_level > 3 SEND evacuation TO Bardiya
"""

token_lines = lex(script)
ast = parse(token_lines)
execute(ast)
print_report()