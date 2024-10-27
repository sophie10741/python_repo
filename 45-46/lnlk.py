def vigenere_decrypt(ciphertext, key):
    decrypted_text = ''
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            # Определяем базу: 65 для A-Z или 97 для a-z
            base = 65 if char.isupper() else 97
            key_char = key[i % key_length].lower()  # используем нижний регистр для ключа
            key_shift = ord(key_char) - 97  # сдвиг по алфавиту
            decrypted_char = chr(((ord(char) - base - key_shift) % 26) + base)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char  # сохраняем не буквенные символы
    return decrypted_text

print(vigenere_decrypt('BkFlSbAmUbuCdTsAmMcMdMdAmMtMdEu', 'Знаетекакзаинтересоватьчеловека'))