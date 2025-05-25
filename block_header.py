from GOST34112018 import GOST341112
from generator import generate_prng
from merkle_tree import build_tree_from_data
import datetime


def time_to_bytes(timestamp):
    current_time = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
    formatted_time = current_time.strftime('%H%d%m%Y')
    time_as_int = int(formatted_time)
    return time_as_int.to_bytes(32, byteorder='big')


block_len = b'c\x8bW\xa3'
prev_block_hash = generate_prng(count=1)[0][0]  # рандомное 256 битное число
merkle_root_hash = build_tree_from_data().root.hash

timestamp_bytes = time_to_bytes("2025-05-26 01:15:58.204125")


def check_condition(hashed_data: bytes):
    """Проверяет, подходит ли хеш (изменяемый nonce) заданному параметру. """
    first_byte = hashed_data[0]
    return (first_byte & 0b11111000) == 0


for nonce_int in range(0, 2 ** 32):
    nonce = nonce_int.to_bytes(32, byteorder='big')
    block_bytes = block_len + prev_block_hash + merkle_root_hash + timestamp_bytes + nonce
    block_hash = GOST341112(block_bytes, digest_size=256).digest()
    if check_condition(block_hash):
        print("Nonce найден!")
        print(nonce_int, nonce)
        print(f"Итоговый хеш блока: {block_hash}")
        break
