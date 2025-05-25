from GOST34112018 import hash_msg
from generator import generate_prng

p = 0x112e06dc10ba8b690ed6ce57b4f4d62510fb
q = 0x897036e085d45b4876b672bda7a6b12887d
g = 0x3


def schnorr_sign(message: bytes, private: int) -> tuple[int, int]:
    public = pow(g, private, p)

    k = int(generate_prng(count=5)[-1], 16)
    R = pow(g, k, p)

    # Преобразование R и P в байты фиксированной длины
    R_bytes = R.to_bytes((R.bit_length() + 7) // 8, 'big')
    P_bytes = public.to_bytes((public.bit_length() + 7) // 8, 'big')

    # Вычисление хэша e = H(R || P || m)
    e_bytes = hash_msg(R_bytes + P_bytes + message)
    e = int.from_bytes(e_bytes, 'big') % q

    s = (k + e * private) % q
    return R, s


# Функция проверки подписи
def schnorr_verify(message: bytes, signature: tuple[int, int], public: int) -> bool:
    R, s = signature

    # Преобразование R и P в байты фиксированной длины
    R_bytes = R.to_bytes((R.bit_length() + 7) // 8, 'big')
    P_bytes = public.to_bytes((public.bit_length() + 7) // 8, 'big')

    # Вычисление хэша e = H(R || P || m)
    e_bytes = hash_msg(R_bytes + P_bytes + message)
    e = int.from_bytes(e_bytes, 'big') % q

    # Проверка: g^s mod p == R * P^e mod p
    left = pow(g, s, p)
    right = (R * pow(public, e, p)) % p

    print(left)
    print(right)

    return left == right


message = b"Test message for Schnorr signature"

private = int(generate_prng(count=1)[-1], 16) % q
public = pow(g, private, p)

signature = schnorr_sign(message, private)
# print(signature)

valid = schnorr_verify(message, signature, public)

print("IS VALID?", valid)
