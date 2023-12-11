import os

def is_mate(fen):
    return fen.split()[-1].startswith('#')



def convert_to_rating(moves, is_black):
    base_rating = 1
    
    if moves.startswith('-'):
        mate_in_moves = abs(int(moves))
        rating = -1 + mate_in_moves * 0.06  
        return max(-1, min(-0.5, rating))  
    else:
        mate_in_moves = int(moves)
        rating = 1 - mate_in_moves * 0.06  
        return min(1, max(0.5, rating))  


def normalize(score):
    value = score / 100
    value/=2
    
    if value >= 0:
        return str(pow(value, 0.6))
    else:
        return str(-pow(abs(value), 0.6))



input_file = r'AI\output_folder\output_1.txt'
output_file = r'AI\processed_data\output_1.txt'
with open(input_file, 'r') as file:
    lines = file.readlines()

fen_exists = set()
counting = 0
output_lines = []
for line in lines:
    fen_row = line.strip()
    realFen = ' '.join(fen_row.split()[:-1])
    if realFen in fen_exists:
        counting+=1
        # continue
    else:
        fen_exists.add(realFen)
    if is_mate(fen_row):
        moves = fen_row.split()[-1][1:]  # Extract number of moves from mate symbol
        is_black = fen_row.split()[-1].startswith('-')
        rating = convert_to_rating(moves, is_black)
        parts = fen_row.split()
        parts[-1] = f'{rating}'  
        fen_row = ' '.join(parts)
    else:
        temp = fen_row.split()[:-1]
        temp.append(normalize(float(fen_row.split()[-1])))
        fen_row = ' '.join(temp)
        # print(fen_row.split()[-1])
    output_lines.append(fen_row + '\n')

print(f"Total duplicate FENs: {counting}")
print(f"Total lines in the input file: {len(lines)}")
print(f"Total lines in the output: {len(output_lines)}")

os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w') as file:
    file.writelines(output_lines)

print(f"Conversion completed. Check '{output_file}' for the updated FEN positions.")