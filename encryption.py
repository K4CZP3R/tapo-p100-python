from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from logger import Logger
from models.key_pair import KeyPair
from tp_link_cipher import TpLinkCipher
import base64, hashlib, helpers


class Encryption:
    def __init__(self):
        self.log = Logger("Encryption")

    @staticmethod
    def __remove_annotations(private_key: str, public_key: str) -> [str, str]:
        private_key = private_key.replace("-----BEGIN PRIVATE KEY-----\n", "")
        private_key = private_key.replace("\n-----END PRIVATE KEY-----", "")
        private_key = private_key.replace("\n", "\r\n")

        public_key = public_key.replace("-----BEGIN PUBLIC KEY-----\n", "")
        public_key = public_key.replace("\n-----END PUBLIC KEY-----", "")
        public_key = public_key.replace("\n", "\r\n")

        return [private_key, public_key]



    def generate_key_pair(self) -> KeyPair:
        key = RSA.generate(1024)
        private_key = key.export_key(pkcs=8, format="DER")
        public_key = key.publickey().export_key(pkcs=8, format="DER")

        # strip down annotations
        private_key = helpers.mime_encoder(private_key)
        public_key = helpers.mime_encoder(public_key)

        self.log.out(f"Generated private_key: {private_key}")
        self.log.out(f"Generated public_key: {public_key}")

        return KeyPair(
            private_key=private_key,
            public_key=public_key
        )

    @staticmethod
    def decode_handshake_key(key: str, key_pair: KeyPair) -> TpLinkCipher:
        decode: bytes = base64.b64decode(key.encode("ASCII"))
        decode2: bytes = base64.b64decode(key_pair.get_private_key())

        cipher = PKCS1_v1_5.new(RSA.import_key(decode2))
        do_final = cipher.decrypt(decode, None)
        if do_final is None:
            raise ValueError("Decryption failed!")

        b_arr: bytearray = bytearray(0)
        b_arr2: bytearray = bytearray(0)

        for i in range(0, 16):
            b_arr.insert(i, do_final[i])
        for i in range(0, 16):
            b_arr2.insert(i, do_final[i+16])

        return TpLinkCipher(b_arr, b_arr2)

    @staticmethod
    def sha_digest_username(data: str):
        b_arr = data.encode("UTF-8")
        digest = hashlib.sha1(b_arr).digest()

        sb = ""
        for i in range(0, len(digest)):
            b = digest[i]
            hex_string = hex(b & 255).replace("0x","")
            if len(hex_string) == 1:
                sb += "0"
                sb += hex_string
            else:
                sb += hex_string
        print(sb)
        return sb
