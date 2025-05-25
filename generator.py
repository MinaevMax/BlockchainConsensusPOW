from GOST34112018 import hash_msg


def to_512bit_block(data: bytes) -> bytes:
    """Дополнение до 64 байт (512 бит) с добавлением длины, как в ГОСТ"""
    bit_len_bytes = (len(data) * 8).to_bytes(8, 'little')
    total_len = len(data) + len(bit_len_bytes)
    if total_len > 64:
        raise ValueError("Входные данные превышают 512 бит")
    padding = bytes(64 - total_len)
    return padding + bit_len_bytes + data


def generate_prng(fullname: str = "Minaev Maxim && Zubov Timofey", count: int = 10):
    # Этап 0: начальное значение h0 = H(512 бит, основанных на ФИО)
    initial_input = to_512bit_block(fullname.encode('utf-8'))
    h0 = hash_msg(initial_input)
    # print(f"ho с именами авторов-студентов: {h0.hex()}")

    # Циклы генерации псевдослучайных чисел
    results = []
    for i in range(1, count + 1):
        i_bytes = i.to_bytes(32, byteorder='little')  # i как 256 бит (32 байта)
        hi = hash_msg(h0 + i_bytes)  # 64 байта (512 бит)
        results.append((hi, hi.hex()))
    return results


def generate_200_bytes_data(input_data: str | None = None):
    """
        Генерирует ровно 200 байт.
        7 конкатенированных вызовов функции generate_prng дадут 224 байта.
        Берем первые 200.
    """
    ans = b''
    if input_data is not None:
        r_values = generate_prng(input_data, count=7)
    else:
        r_values = generate_prng(count=7)
    for bytes_val, _ in r_values:
        ans += bytes_val
    return ans[:200]


if __name__ == "__main__":
    fullname = "Minaev Maxim && Zubov Timofey"
    prng_values = generate_prng(fullname, count=5)

    for idx, val in enumerate(prng_values, start=1):
        print(f"Псевдослучайное число h{idx}: {val[1]}")
