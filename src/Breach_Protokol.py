import time
import random

##################################################################### READ ##################################################
def read_file_to_string(file_path):
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
        return file_contents
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error:{e}")
        return None

def main_reader_txt(file_path):
    file_content = read_file_to_string(file_path)

    buffer_size = int(file_content[0])
    matrix_width = int(file_content[2])
    matrix_length = int(file_content[4])

    matrix_idx = 6
    matrix = []
    for i in range(matrix_length):
        a = []
        for j in range(matrix_width):
            a.append(file_content[matrix_idx] + file_content[matrix_idx + 1])
            matrix_idx += 3
        matrix.append(a)

    number_of_sequences = int(file_content[matrix_idx])
    sequences = []
    matrix_idx += 2

    for i in range(number_of_sequences):
        string = ''
        while file_content[matrix_idx] != '\n':
            string += file_content[matrix_idx]
            matrix_idx += 1

        matrix_idx += 1

        score = ''
        while (file_content[matrix_idx] != '\n') and (matrix_idx < len(file_content) - 1):
            score += file_content[matrix_idx]
            matrix_idx += 1

        if matrix_idx == len(file_content) - 1:
            score += file_content[matrix_idx]

        if i != number_of_sequences - 1:
            matrix_idx += 1

        sequences.append((string.split(), score))

    return matrix, buffer_size, sequences

##################################################################### SOLVER ##################################################
def is_valid_move(matrix, pos, row, col):
    rows = len(matrix)
    cols = len(matrix[0])
    return 0 <= row < rows and 0 <= col < cols and not pos[row][col]


def find_paths(matrix, pos, row, col, length, path, coor, all_paths, all_coor, direction):
    if length == 0:
        all_paths.append(path[:])
        all_coor.append(coor[:])
        return

    pos[row][col] = True

    if direction == 'horizontal':
        horizontal_dir = []

        for i in range(1, len(matrix[0])):
            horizontal_dir.append((0, i))
            horizontal_dir.append((0, i * -1))

        # Horizontal movements
        for dr, dc in horizontal_dir:
            new_row, new_col = row + dr, col + dc
            if is_valid_move(matrix, pos, new_row, new_col):
                path.append(matrix[new_row][new_col])
                coor.append((new_col + 1, new_row + 1))
                find_paths(matrix, pos, new_row, new_col, length - 1, path, coor, all_paths, all_coor, 'vertical')
                path.pop()
                coor.pop()
    else:
        vertical_dir = []

        for i in range(1, len(matrix[0])):
            vertical_dir.append((i, 0))
            vertical_dir.append((i * -1, 0))

        # Vertical movements
        for dr, dc in vertical_dir:
            new_row, new_col = row + dr, col + dc
            if is_valid_move(matrix, pos, new_row, new_col):
                path.append(matrix[new_row][new_col])
                coor.append((new_col + 1, new_row + 1))
                find_paths(matrix, pos, new_row, new_col, length - 1, path, coor, all_paths, all_coor, 'horizontal')
                path.pop()
                coor.pop()

    pos[row][col] = False

def find_all_paths(matrix, length):
    rows = len(matrix)
    cols = len(matrix[0])
    all_paths = []
    all_coor = []

    for j in range(cols):  # Iterate over cells in the first row only
        pos = [[False] * cols for _ in range(rows)]
        path = [matrix[0][j]]
        coor = [(j + 1, 1)]
        find_paths(matrix, pos, 0, j, length - 1, path, coor, all_paths, all_coor, 'vertical')

    return (all_paths, all_coor)

def isSublist(lst, sub):
    if not sub:
        return True
    if not lst:
        return False

    for i in range(len(lst)):
        if lst[i:i + len(sub)] == sub:
            return True

    return False

def max_index(lst):
    if not lst:
        return None  # Return None if the list is empty
    max_value = max(lst)
    max_index = lst.index(max_value)
    return max_index

def main_solver_txt(matrix, buffer_size, sequences):
    start = time.time()
    all_paths = find_all_paths(matrix, buffer_size)[0]
    all_coor = find_all_paths(matrix, buffer_size)[1]

    score_path = []
    for path in all_paths:
        temp_score = 0
        for sequence in sequences:
            if isSublist(path, sequence[0]):
                temp_score += int(sequence[1])
        score_path.append(temp_score)

    #Print the optimal solution
    str = f"{max(score_path)}\n"

    str += f"{' '.join(all_paths[max_index(score_path)])}\n"

    for coor in all_coor[max_index(score_path)]:
        str += f"{coor[0]}, {coor[1]}\n"

    end = time.time()
    res = end - start
    final_res = res * 1000

    str += f"\n{final_res} ms"

    print(f"\n{str}")
    return str

def random_matrix(rows, cols, elements):
    matrix = []
    for _ in range(rows):
        row = [random.choice(elements) for _ in range(cols)]
        matrix.append(row)

    return matrix

def random_sequence(token, seq_max_size, seq):
    a = [random.choice(token) for _ in range(random.randint(2, seq_max_size))]

    #Loop to ensure that every sequence is unique
    loop_stat = False
    while not loop_stat:
        if a in seq:
            a = [random.choice(token) for _ in range(random.randint(2, seq_max_size))]
        else:
            loop_stat = True

    return a

def save_string_to_file(string, filename):
    with open(filename, 'w') as file:
        file.write(string)

def main_solver_cli():
    numof_unique_tokens = int(input("Jumlah Token: "))

    token = []
    for i in range(numof_unique_tokens):
        token.append(input(f"Token {i + 1}: "))

    buffer_size = int(input("Ukuran Buffer: "))
    # Meminta masukan dari pengguna
    input_string = input("Masukkan jumlah baris dan kolom (dipisahkan spasi): ")
    # Memisahkan masukan menjadi baris dan kolom
    matrix_row, matrix_column = map(int, input_string.split())
    matrix = random_matrix(matrix_row, matrix_column, token)

    numof_sequence = int(input("Jumlah Sekuens: "))
    seq_max_size = int(input("Ukuran Sekuens: "))

    start = time.time()

    seq = []
    for _ in range(numof_sequence):
        a = random_sequence(token, seq_max_size, seq)
        seq.append(a)

    seq_value = [random.randint(10, 50) for _ in range(len(seq))]

    all_paths = find_all_paths(matrix, buffer_size)[0]
    all_coor = find_all_paths(matrix, buffer_size)[1]

    score_path = []
    for path in all_paths:
        temp_score = 0
        for sequence in seq:
            if isSublist(path, sequence):
                temp_score += int(seq_value[seq.index(sequence)])
        score_path.append(temp_score)

    # Print the matrix and sequence
    print("")
    str = "Matrix:\n"

    for row in matrix:
        str += f"{row}\n"

    str += f"\nSequence:\n"

    for i in range(len(seq)):
        str += f"{seq[i]}\n"
        str += f"{seq_value[i]}\n"

    str += f"\n{max(score_path)}\n{' '.join(all_paths[max_index(score_path)])}\n"
    save_str = f"{max(score_path)}\n{' '.join(all_paths[max_index(score_path)])}\n"

    for coor in all_coor[max_index(score_path)]:
        str += f"{coor[0]}, {coor[1]}\n"
        save_str += f"{coor[0]}, {coor[1]}\n"

    end = time.time()
    res = end - start
    final_res = res * 1000

    str += f"\n{final_res} ms"
    save_str += f"\n{final_res} ms"

    print(str)
    return save_str

##################################################################### MAIN ##################################################

print("1. TXT File")
print("2. CLI")
input_mode = input("Pilih metode: ")

str = ""
if input_mode == "1":
    file_path = input("File path: ")
    dir_file_path = "D:\\Semester 4 - Teknik Informatika\\IF2211 - Strategi Algoritma\\Tucil1_13522154\\test" + file_path
    file_content = main_reader_txt(dir_file_path)
    str += main_solver_txt(file_content[0], file_content[1], file_content[2])
elif input_mode == "2":
    str += main_solver_cli()

save_stat = input("Apakah anda ingin menyimpan solusi ini? (Y/N) ")
if save_stat.upper() == "Y":
    file_name = input("Input nama file: ")
    dir_file = "D:\\Semester 4 - Teknik Informatika\\IF2211 - Strategi Algoritma\\Tucil1_13522154\\test" + file_name
    print("Saving...")
    save_string_to_file(str, dir_file)
    print("Saved!")

elif save_stat.upper() == "N":
    print("not saved")
    exit()
