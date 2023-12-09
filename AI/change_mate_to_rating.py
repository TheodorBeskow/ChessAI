import os

def is_mate(fen):
    return fen.split()[-1].startswith('#')



def convert_to_rating(moves, is_black):
    base_rating = 10000
    
    if moves.startswith('-'):
        mate_in_moves = abs(int(moves))
        rating = -10000 + mate_in_moves * 300  # Adjust the rating for black's mate-in-# moves
        return max(-10000, min(-2000, rating))  # Cap the rating for black's mate-in-# between -10000 and -2000
    else:
        mate_in_moves = int(moves)
        rating = 10000 - mate_in_moves * 300  # Adjust the rating for white's mate-in-# moves
        return min(10000, max(2000, rating))  # Cap the rating for white's mate-in-# between 10000 and 2000




input_file = 'AI\output_folder\output_1.txt'
output_file = 'AI\processed_data\output_1.txt'
with open(input_file, 'r') as file:
    lines = file.readlines()

output_lines = []
for line in lines:
    fen_row = line.strip()
    if is_mate(fen_row):
        moves = fen_row.split()[-1][1:]  # Extract number of moves from mate symbol
        is_black = fen_row.split()[-1].startswith('-')
        rating = convert_to_rating(moves, is_black)/100
        parts = fen_row.split()
        parts[-1] = f'{rating}'  # Replace mate symbol with the adjusted rating
        fen_row = ' '.join(parts)
    output_lines.append(fen_row + '\n')

print(f"Total lines in the input file: {len(lines)}")
print(f"Total lines in the output: {len(output_lines)}")

os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w') as file:
    file.writelines(output_lines)

print(f"Conversion completed. Check '{output_file}' for the updated FEN positions.")