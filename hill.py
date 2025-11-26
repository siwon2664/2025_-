import string
import numpy as np

#평문 P,  키 K, 암호문 C
# C = K*P(mod 26)
#복호화 공식 = P = K^-1 *C(mod 26)
# det(K)와 26은 서로소여야 한다.
#
#알파벳 리스트
alphabet = [i for i in string.ascii_lowercase]
plain_text = ""


# 행렬의 문자를 숫자로 바꿔줌 
def text_to_number(matrix):
    number_matrix = []
    for row in matrix:
        number_row = []
        for ch in row:
            if ch in alphabet:
                number_row.append(alphabet.index(ch))
        number_matrix.append(number_row)
    return number_matrix

def text_to_number(matrix, alphabet):
    number_matrix = []
    for row in matrix:
        number_row = []
        for ch in row:
            number_row.append(alphabet.index(ch))
        number_matrix.append(number_row)
    return number_matrix

# hill암호화
def hill_encrypt(K, P):
    """
    K:  키 
    P: 평문 
    """
    P = np.array(P).reshape(-1,1)
    C = np.dot(K,P) % 26
    return C.flatten()
# hill 복호화
def hill_decrypt(K,C,m =26):



#encryption
#key_matrix = np.array() 


#decryption

#main
# n = int(input("행렬의 크기 n을 입력하세요 (n x n 행렬): "))
# print(f"{n}x{n} 행렬에 들어갈 {n*n}개의 숫자를 공백으로 구분하여 입력하세요:")
# values = list(map(int, input().split()))
# if len(values) != n * n:
#     raise ValueError(f"값의 개수가 맞지 않습니다! {n*n}개 입력해야 합니다.")
# key_matrix = np.array(values).reshape(n, n)
# print("\n입력된 키 행렬:")
# print(key_matrix)

    