data = """
T 193.23.143.43:23566 -> 10.0.0.2:1433 [AP]
  12 01 00 2f 00 00 01 00    00 00 1a 00 06 01 00 20    .../...........
  00 01 02 00 21 00 01 03    00 22 00 04 04 00 26 00    ....!...."....&.
  01 ff 09 00 00 00 00 00    00 00 00 00 00 48 00       .............H.

T 10.0.0.2:1433 -> 193.23.143.43:23566 [AP]
  04 01 00 25 00 00 01 00    00 00 15 00 06 01 00 1b    ...%............
  00 01 02 00 1c 00 01 03    00 1d 00 00 ff 08 00 07    ................
  f7 00 00 02 00                                        .....

T 193.23.143.43:23566 -> 10.0.0.2:1433 [AP]
  10 01 01 56 00 00 01 00    4e 01 00 00 02 00 09 72    ...V....N......r
  ...
"""

# Преобразование в байты и декодирование
import re

# Извлечение всех байтов
hex_data = re.findall(r'([0-9A-Fa-f]{2})', data)
byte_array = bytearray(int(b, 16) for b in hex_data)

# Декодирование
try:
    decoded_text = byte_array.decode('utf-16', errors='ignore')
    print(decoded_text)
except Exception as e:
    print(f"Ошибка декодирования: {e}")