from GOST34112018 import hash_msg
from generator import generate_prng

# Параметры
p = int("ee8172ae854510e2ea0a12b36bb0c3458996608f977a4d6343e9190fd165976e"
        "b69359b8bc97322c23177539f2195ec99eb82a69e5dc338684583978b1c379e3", 16)

q = int("98915e7eb064bdc7c8265edf285dd50dcda31e887289f0acf24809dd6f49dd2d", 16)

g = int("9e960315afad2538067559848ebe2cd400c8774ab4b6270aa49e50936ac3d849"
        "869582d46f7c883704d648be5b142aa6afde2127b50d50f22ab5aab1ce23e21c", 16)


# Сделаноо по алгоритму из ВИКИ(не заработало), алгоритм из доки по практике схожий(но тоже не работает): 
# https://ru.wikipedia.org/wiki/%D0%A1%D1%85%D0%B5%D0%BC%D0%B0_%D0%A8%D0%BD%D0%BE%D1%80%D1%80%D0%B0#:~:text=%D0%B4%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%20%D0%BD%D0%B5%20%D1%83%D0%B4%D0%B0%D0%BB%D0%BE%D1%81%D1%8C.-,%D0%9F%D1%80%D0%BE%D1%82%D0%BE%D0%BA%D0%BE%D0%BB%20%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8,-%5B%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D1%82%D1%8C%20%7C

# --- Подпись ---
def wiki_schnorr_sign(message: bytes, r:int, x: int, w: int):
    x_bytes = x.to_bytes((p.bit_length() + 7) // 8, 'big')

    s1 = int(hash_msg(message+ x_bytes).hex(), 16)
    s2 = (r + w * s1) % q

    return (s1, s2)

def wiki_schnorr_verify(message: bytes, y: int, signature: tuple[int, int]) -> bool:
    s1, s2 = signature
    X = pow(g, s2, p) * pow(y, s1, p) % p
    left = int(hash_msg(message + bytes.fromhex(hex(X)[2:])).hex(), 16)
    
    print(left)
    print(s1)

    return left == s1

def schnorr_sign(message: bytes, x: int) -> tuple[int, int]:
    r = int(generate_prng(count=1)[0], 16) 
    R = pow(g, r, p)

    # Преобразование R и P в байты фиксированной длины
    blen = (p.bit_length() + 7) // 8
    R_bytes = R.to_bytes(blen, 'big')
    P = pow(g, x, p)
    P_bytes = P.to_bytes(blen, 'big')

    # Вычисление хэша e = H(R || P || m)
    e_bytes = hash_msg(R_bytes + P_bytes + message)
    e = int.from_bytes(e_bytes, 'big') % q

    s = (r + e * x) % q
    return R, s

# Функция проверки подписи
def schnorr_verify(message: bytes, signature: tuple[int, int], P: int) -> bool:
    R, s = signature

    # Преобразование R и P в байты фиксированной длины
    blen = (p.bit_length() + 7) // 8
    R_bytes = R.to_bytes(blen, 'big')
    P_bytes = P.to_bytes(blen, 'big')

    # Вычисление хэша e = H(R || P || m)
    e_bytes = hash_msg(R_bytes + P_bytes + message)
    e = int.from_bytes(e_bytes, 'big') % q

    # Проверка: g^s mod p == R * P^e mod p
    left = pow(g, s, p)
    right = (R * pow(P, e, p)) % p
    
    print(left)
    print(right)

    return left == right

message = b"Hello World!"

r_bytes = generate_prng(count=1)[0]
r = int(r_bytes, 16) % q
x = pow(g, r, p)

# секретный ключ Пегги
w_bytes = generate_prng(count=2)[0]
w = int(r_bytes, 16) % q

y = pow(g, q-w, p)

signature = schnorr_sign(message, r)
#print(signature)

valid = schnorr_verify(message, signature, x)

#signature = wiki_schnorr_sign(message, r, x, w)
#print(signature)

#valid = wiki_schnorr_verify(message, y, signature, x)
print("IS VALID?", valid)