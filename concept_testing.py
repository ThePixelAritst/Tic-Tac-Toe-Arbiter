import hashlib

with open(r"D:\Coding adventures\Tic Tac Arbiter\Engine_base\Engine_communications.py", "rb") as file_1:
    digest_file_1 = hashlib.file_digest(file_1, "sha256")
    digested_1 = digest_file_1.hexdigest()

with open(r"D:\Coding adventures\Tic Tac Arbiter\Resources\engine_comms.py", "rb") as file_2:
    digest_file_2 = hashlib.file_digest(file_2, "sha256")
    digested_2 = digest_file_2.hexdigest()

if digested_1 == digested_2:
    print("same")
else:
    print("different")