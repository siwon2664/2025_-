import numpy as np
import string
#평문 P,  키 K, 암호문 C
# C = K*P(mod 26)
#복호화 공식 = P = K^-1 *C(mod 26)
# det(K)와 26은 서로소여야 한다.
#

K = [
    ['a','f'],
    ['z','f']
]
alphabet = string.ascii_lowercase
alphabet_map = {ch: idx for idx, ch in enumerate(alphabet)}
plaintext = "attackatdawn"
#알파벳을 숫자로 변환
def text_to_number(matrix):
    number_matrix = []
    for row in matrix:
        # row가 리스트면 문자열로 합쳐주기
        if isinstance(row, list):
            row = "".join(row)

        # row가 문자열이라고 가정하고 처리
        number_row = []
        for ch in row.lower():  
            if ch in alphabet_map:
                number_row.append(alphabet_map[ch])
        number_matrix.append(number_row)
    
    return number_matrix

#키를 기반으로 블록 나누기
def make_blocks_by_key(num_list, key_matrix, pad=23):
    # block_size = 키 행렬의 열 개수
    block_size = len(key_matrix[0])
    
    blocks = []
    for i in range(0, len(num_list), block_size):
        block = num_list[i:i + block_size]
        if len(block) < block_size:
            block += [pad] * (block_size - len(block))
        blocks.append(block)
# 행렬화된 평문 return
    return blocks


def hill_encrypt(block, key_matrix):
    # C = K*P(mod 26)
    size = len(key_matrix)  # 키 행렬의 크기
    result = [0] * size

    for i in range(size):
        total = 0
        for j in range(size):
            total += key_matrix[i][j] * block[j]
        result[i] = total % 26
    
    return result
def number_to_text(num_list):
    return "".join(alphabet[n] for n in num_list)


# ----- 여기서부터 실제 동작 -----

# 1) 평문 -> 숫자
nums = text_to_number([plaintext])[0]   # [0,19,19,0,2,10,...]

# 2) 문자 키 -> 숫자 키
K_num = text_to_number(K)                # [[0,5],[25,5]]

# 3) 키에 맞게 블록 나누기
blocks = make_blocks_by_key(nums, K_num)

# 4) 각 블록을 암호화
cipher_blocks = []
for block in blocks:
    cipher_blocks.append(hill_encrypt(block, K_num))

# 5) 블록들을 평평하게 펼치기 (2차원 -> 1차원)
cipher_nums = [n for block in cipher_blocks for n in block]

# 6) 숫자 -> 문자로 변환해서 최종 암호문 만들기
ciphertext = number_to_text(cipher_nums)

print("평문 :", plaintext)
print("평문 숫자 :", nums)
print("키 (숫자) :", K_num)
print("블록들 :", blocks)
print("암호 숫자 :", cipher_nums)
print("암호문 :", ciphertext)