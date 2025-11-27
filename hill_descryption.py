import numpy as np
import string

# 암호문과 키(문자)
ciphertext = "rrahywrraxnr"
K = [
    ['a', 'f'],
    ['z', 'f']
]

alphabet = string.ascii_lowercase
alphabet_map = {ch: idx for idx, ch in enumerate(alphabet)}

# 1) 알파벳 → 숫자
def text_to_number(matrix):
    number_matrix = []
    for row in matrix:
        # row가 리스트면 문자열로 합쳐주기 (키 행렬도 처리 가능)
        if isinstance(row, list):
            row = "".join(row)

        number_row = []
        for ch in row.lower():
            if ch in alphabet_map:
                number_row.append(alphabet_map[ch])
        number_matrix.append(number_row)
    return number_matrix

# 2) 숫자 → 알파벳
def number_to_text(num_list):
    return "".join(alphabet[n] for n in num_list)

# 3) 키에 맞게 블록 나누기
def make_blocks_by_key(num_list, key_matrix, pad=23):
    block_size = len(key_matrix[0])  # 열 개수 = 블록 크기
    blocks = []
    for i in range(0, len(num_list), block_size):
        block = num_list[i:i + block_size]
        if len(block) < block_size:
            block += [pad] * (block_size - len(block))
        blocks.append(block)
    return blocks

# 4) 모듈러 역원 (det^-1)
def modinv(a, m=26):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:   # 1 이 되어야 함!
            return x
    return None

# 5) 키 역행렬 계산 (일반 n×n, 여기선 2×2)
def inverse_key_matrix(K_num):
    M = np.array(K_num)
    det = int(round(np.linalg.det(M)))   # 정수화
    det_mod = det % 26
    inv_det = modinv(det_mod, 26)
    if inv_det is None:
        raise ValueError("det(K)와 26이 서로소가 아니라 역행렬이 없습니다.")

    # adj(M) = det(M) * M^-1
    adj = np.round(det * np.linalg.inv(M)).astype(int)
    inv_M = (inv_det * adj) % 26
    return inv_M.tolist()

# 6) 블록 하나 복호화
def hill_decrypt(block, inv_key_matrix):
    size = len(inv_key_matrix)
    plain_block = [0] * size
    for i in range(size):
        total = 0
        for j in range(size):
            total += inv_key_matrix[i][j] * block[j]
        plain_block[i] = total % 26
    return plain_block

# ----- 여기서부터 실제 복호화 동작 -----

# 키 문자 → 숫자
K_num = text_to_number(K)              # 예: [[0,5],[25,5]]

# 역키 행렬 계산 (mod 26)
inv_key_matrix = inverse_key_matrix(K_num)

# 1) 암호문 → 숫자
cipher_nums = text_to_number([ciphertext])[0]

# 2) 암호문 블록 나누기
cipher_blocks = make_blocks_by_key(cipher_nums, K_num)

# 3) 각 블록 복호화
plain_blocks = [hill_decrypt(b, inv_key_matrix) for b in cipher_blocks]

# 4) 2차원을 1차원으로 평탄화
plain_nums = [n for block in plain_blocks for n in block]

# 5) 숫자 → 문자열
plaintext_dec = number_to_text(plain_nums)

print("[복호화 과정]")
print("암호문       :", ciphertext)
print("암호문 숫자  :", cipher_nums)
print("암호 블록들  :", cipher_blocks)
print("역키 행렬    :", inv_key_matrix)
print("복호 숫자    :", plain_nums)
print("복호문       :", plaintext_dec)
