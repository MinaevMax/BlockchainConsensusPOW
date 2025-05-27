from GOST34112018 import hash_msg
from generator import generate_prng

p = int("EE8172AE8996608FB69359B89EB82A69854510E2977A4D63BC97322CE5DC3386"
        "EA0A12B343E9190F23177539845839786BB0C345D165976EF2195EC9B1C379E3", 16)

q = int("98915E7EC8265EDFCDA31E88F24809DDB064BDC7285DD50D7289F0AC6F49DD2D", 16)

g = int("9E96031500C8774A869582D4AFDE2127AFAD2538B4B6270A6F7C8837B50D50F2"
        "06755984A49E509304D648BE2AB5AAB18EBE2CD46AC3D8495B142AA6CE23E21C", 16)

def schnorr_sign(message: bytes, private: int) -> tuple[int, int]:
    public = pow(g, private, p)

    k = int(generate_prng(count=5)[-1][1], 16)
    R = pow(g, k, p)

    # Преобразование R и P в байты фиксированной длины
    R_bytes = R.to_bytes((R.bit_length() + 7) // 8, 'big')
    P_bytes = public.to_bytes((public.bit_length() + 7) // 8, 'big')

    # Вычисление хэша e = H(R || P || m)
    e_bytes = hash_msg(R_bytes + P_bytes + message)
    e = int.from_bytes(e_bytes, 'big') % q

    s = (k + e * private) % q
    return R, s


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

    # print(left)
    # print(right)

    return left == right


if __name__ == '__main__':
    message = b"Test message for Schnorr signature"
    private = int(generate_prng(count=1)[-1][1], 16) % q
    public = pow(g, private, p)

    signature = schnorr_sign(message, private)
    # print(signature)

    valid = schnorr_verify(message, signature, public)

    print("IS VALID?", valid)
