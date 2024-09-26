
def generate_pems():
	# Генерация пары ключей
	private_key = rsa.generate_private_key(
		public_exponent=65537,
		key_size=2048
	)

	# Приватный ключ с паролем
	password = str(
		input('Введите пароль для приватного ключа:\n')
	).encode()  # Пароль для шифрования приватного ключа
	salt = os.urandom(16)  # Соль для KDF (ключевое расширение)
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=100_000,
		backend=default_backend()
	)

	key_encryption = serialization.BestAvailableEncryption(password)

	# Сохранение приватного ключа в PEM формате с паролем
	private_pem = private_key.private_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PrivateFormat.PKCS8,
		encryption_algorithm=key_encryption
	)

	# Сохранение публичного ключа в PEM формате
	public_key = private_key.public_key()
	public_pem = public_key.public_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
	)
	# Запись PEM ключей в файлы (при необходимости)
	while True:	
		check_save = input('Хотите сохранить ключи в текущую папку ?\n1/2 (ДА)/(НЕТ)\n')
		if check_save == '1':
			try:
				print(111111)
				with open("private_key_with_password.pem", "w") as f:
					f.write(private_pem.decode())
				with open("public_key.pem", "w") as f:
					f.write(public_pem.decode())
				print('Ключи сохранены в текущую папку')
				break
			except Exception as err:
				print('Несуществующий путь/Недостаточно прав', err)
		elif check_save == '2':
			pwd = input('Введите путь для сохранения ключей:\n')
			try:	
				with open(f"{pwd}/private_key_with_password.pem", "wb") as f:
					f.write(private_pem)
				with open(f"{pwd}/public_key.pem", "wb") as f:
					f.write(public_pem)
				print(f'Ключи сохранены:\n{pwd}')
				break
			except Exception as err:
				print('Несуществующий путь/Недостаточно прав', err)
		else:
			print("Неверный выбор")

def encoding_final(public_key):
	while True:
		message = input(f'''
Выберите действие:\n
1 Ввести текст для шифрования\n
2 Ввести имя файла для шифрования\n
'''
			)
		if message == '1':
			plaintext = input('Введите текст для шифрования:\n')
		elif message == '2':
			a = input('Введите имя файла для шифрования:\n')
			with open(a, 'r') as file:
				plaintext = file.read()
		else:
			print('Неверный выбор')
		try:
			final_public_key = serialization.load_pem_public_key(
					public_key
				)
			ciphertext = final_public_key.encrypt(
				plaintext.encode(),
				padding.OAEP(
					mgf=padding.MGF1(algorithm=hashes.SHA256()),
					algorithm=hashes.SHA256(),
					label=None
					)
				)
			wt = input('Введите название файла для сохранения:\n')
			with open(wt, 'w') as file:
				file.write(base64.b64encode(ciphertext).decode('utf-8'))
			print('Файл успешно зашифрован и сохранен')
			break	
		except Exception as err:
			print('PEM файл поврежден, не удалось открыть', err)
			break
		


def encoding_text():
	while True:
		pwd = input('Публичный ключ находится в этой папке ?\n1/2 (ДА)/(НЕТ)\n')
		if pwd == '1':
			try:
				wt = input('Введите полное название публичного ключа:\n')
				with open(wt, 'r') as file:
					encoding_final(file.read().encode())
				break
			except Exception as err:
				print('Файла несуществует')
		elif pwd == '2':
			try:
				wt = input('Введите путь до публичного ключа:\n')
				with open(wt, 'r') as file:
					encoding_final(file.read().encode())
				break
			except Exception as err:
				print('Неверный путь/Файла не несуществует')
		else:
			print('Неверный выбор')

def decoding_final(pr):
	while True:
		try:
			private_key = serialization.load_pem_private_key(
				pr,
				password=input('Введите пароль от публичного ключа:\n').encode()
			)
			pwd = input('Файл для декодирования находится в этой папке ?\n1/2 (ДА)/(НЕТ)\n')
			if pwd == '1':
				pwd_file = input('Введите полное название файла для декодирования:\n')
			elif pwd == '2':
				pwd_file = input('Введите полный путь до файла для декодирования:\n')
			else:
				print('Неверный выбор')
			try:
				with open(pwd_file, 'r') as file:
					text = file.read()

				# Decode the Base64 ciphertext
				decoded_ciphertext = base64.b64decode(text)
				print(decoded_ciphertext)
				plaintext = private_key.decrypt(
					decoded_ciphertext,
					padding.OAEP(
						mgf=padding.MGF1(algorithm=hashes.SHA256()),
						algorithm=hashes.SHA256(),
						label=None
					)
				)
				wt = input('Введите имя файла для сохранения:\n')
				with open(wt, 'w') as file:
					file.write(plaintext.decode())
				print('Файл успешно декодирован и сохранен')
				break
			except Exception as err:
				print('Неверный путь/Название файла', err)
		except Exception as err:
			print('Неверный пароль от публичного ключа', err)


def decoding_text():
	while True:
		pwd = input('Приватный ключ находится в этой папке ? \n1/2 (ДА)/(НЕТ)\n')
		if pwd == '1':
			wt = input('Введите полное название публичного ключа:\n')
			with open(wt, 'r') as file:
				decoding_final(file.read().encode())
			break
		elif pwd == '2':
			wt = input('Введите путь до публичного ключа:\n')
			with open(wt, 'r') as file:
				decoding_final(file.read().encode())
			break
		else:
			print('Неверный выбор')

def main():
	while True:
		ans = input(f'''
Выберите действие:\n
1 (Генеранция ключей)\n
2 (Шифрования текста)\n
3 (Дешифрация текса)\n'''
		)
		if ans == '1':
			generate_pems()
		elif ans == '2':
			encoding_text()
		elif ans == '3':
			decoding_text()
		else:
			print("Неверный	выбор")

if __name__ == '__main__':
	from cryptography.hazmat.primitives.asymmetric import rsa, padding
	from cryptography.hazmat.primitives import serialization
	from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
	from cryptography.hazmat.primitives import hashes
	from cryptography.hazmat.backends import default_backend
	import os, base64
	main()