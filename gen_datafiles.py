import os.path

from generator import generate_200_bytes_data, generate_prng
from schnorr_scheme import schnorr_sign, schnorr_verify, p, q, g

dir = "data"


def sign_file(file_name):
    private = int(generate_prng(count=1)[-1][1], 16) % q
    # public = pow(g, private, p)
    with open(file_name, "rb") as f:
        data = f.read()
        keys = schnorr_sign(data, private)
        gen_filename = ''.join(file_name.split('.')[:-1]) + '_signed.sig'
        with open(gen_filename, "wb") as fw:
            signed_data = data + keys[0].to_bytes(32, byteorder='big') + keys[1].to_bytes(32, byteorder='big')
            fw.write(signed_data)
    return gen_filename, len(signed_data)


def verify_file(file_name):
    private = int(generate_prng(count=1)[-1][1], 16) % q
    public = pow(g, private, p)

    with open(file_name, "rb") as f:
        all_data = f.read()
        data = all_data[:200]
        keyR = all_data[len(data):len(data) + 32]
        keyS = all_data[len(data) + 32:]
        verified = schnorr_verify(data, (int.from_bytes(keyR, byteorder='big'), int.from_bytes(keyS, byteorder='big')),
                                  public)
        return verified


if __name__ == "__main__":
    if not os.path.exists(dir):
        os.makedirs(dir)
    fullname = "Minaev Maxim && Zubov Timofey"
    for idx in range(5):
        filename = f"{dir}/tx_{idx + 1}.bin"
        tx_data = generate_200_bytes_data(fullname + str(idx))

        if idx == 4:
            fullname_bytes = fullname.encode('utf-8')
            tx_data = fullname_bytes + tx_data[len(fullname_bytes):]

        with open(filename, "wb") as f:
            f.write(tx_data)
        print(f"Файл {filename} создан ({len(tx_data)} байт)")

        # print(tx_data == open(filename, 'rb').read())  # байты те же
        sig_file, sig_len = sign_file(filename)
        print(f'Создан файл с подписью Шнорра {sig_file}. Размер ({sig_len})')
        print(f'Файл {sig_file} верифицирован? - {verify_file(sig_file)}')
