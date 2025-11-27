# hill.py  (메인 실행 파일)

from hill_encryption import text_to_number, number_to_text, hill_encrypt_block
from hill_descryption import hill_decrypt, text_to_number as txt2num_dec, number_to_text as num2txt_dec
import numpy as np

# -----------------------------
# 키 행렬 입력
# -----------------------------
print("=== Hill Cipher 실행 ===")
print("키 행렬을 입력하세요 (예: a f / z f )")

# 2x2 문자 입력 예시:
# a f
# z f
key = []
for i in range(2):  # 2x2 기준
    row = input(f"{i+1}번째 행 입력: ").split()
    key.append(row)

# 문자 키 → 숫자 키 변환
key_numbers = text_to_number(key)   # [[0,5],[25,5]]

print("\n숫자 키 행렬:")
print(key_numbers)

# -----------------------------
# 역행렬 계산 (mod 26)
# -----------------------------
matrix = np.array(key_numbers)
det = int(round(np.linalg.det(matrix)))

# det mod 26의 역원 찾기
def modinv(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 26 % m:
            return x
    return None

det_inv = modinv(det)

if det_inv is None:
    print("det(K)와 26이 서로소가 아니라 역행렬이 존재하지 않습니다.")
    exit()

adj = np.round(det * np.linalg.inv(matrix)).astype(int)
inv_key_matrix = (det_inv * adj) % 26

print("\n역행렬 (mod 26):")
print(inv_key_matrix)

# -----------------------------
# 평문 입력 → 암호화
# -----------------------------
plaintext = input("\n평문 입력: ")

nums = text_to_number([plaintext])[0]

block_size = len(key_numbers[0])
blocks = [nums[i:i+block_size] for i in range(0, len(nums), block_size)]

if len(blocks[-1]) < block_size:
    blocks[-1] += [23] * (block_size - len(blocks[-1]))

cipher_blocks = [hill_encrypt_block(b, key_numbers) for b in blocks]
cipher_nums = [n for block in cipher_blocks for n in block]
ciphertext = number_to_text(cipher_nums)

print("\n암호문:", ciphertext)

# -----------------------------
# 복호화
# -----------------------------
plain_blocks = [hill_decrypt(b, inv_key_matrix.tolist()) for b in cipher_blocks]
plain_nums = [n for block in plain_blocks for n in block]
plaintext_restored = number_to_text(plain_nums)

print("복호문:", plaintext_restored)
print("\n=== 실행 완료 ===")
