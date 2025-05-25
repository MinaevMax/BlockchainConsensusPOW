import os.path

from generator import generate_200_bytes_data

dir = "./data"


if __name__ == "__main__":
    if not os.path.exists(dir):
        os.makedirs(dir)
    fullname = "Minaev Maxim && Zubov Timofey"
    for idx in range(5):
        filename = f"{dir}/tx_{idx+1}.bin"
        tx_data = generate_200_bytes_data(fullname + str(idx))

        if idx == 4:
            fullname_bytes = fullname.encode('utf-8')
            tx_data = fullname_bytes + tx_data[len(fullname_bytes):]

        with open(filename, "wb") as f:
            f.write(tx_data)
        print(f"Файл {filename} создан ({len(tx_data)} байт)")

        # print(tx_data == open(filename, 'rb').read())  # байты те же
