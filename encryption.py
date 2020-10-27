from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from models.key_pair import KeyPair
from tp_link_cipher import TpLinkCipher
import base64, hashlib, helpers, logging

logger = logging.getLogger('root')

class Encryption:
    def generate_key_pair(self) -> KeyPair:
        logger.debug(f"Generating key...")
        key = RSA.generate(1024)
        private_key = key.export_key(pkcs=8, format="DER")
        public_key = key.publickey().export_key(pkcs=8, format="DER")

        logger.debug("MIME encoding private and public key...")
        private_key = helpers.mime_encoder(private_key)
        public_key = helpers.mime_encoder(public_key)

        return KeyPair(
            private_key=private_key,
            public_key=public_key
        )

    @staticmethod
    def decode_handshake_key(key: str, key_pair: KeyPair) -> TpLinkCipher:
        logger.debug(f"Will decode handshake key (...{key[5:]}) using current key pair")
        decode: bytes = base64.b64decode(key.encode("UTF-8"))
        decode2: bytes = base64.b64decode(key_pair.get_private_key())

        cipher = PKCS1_v1_5.new(RSA.import_key(decode2))
        do_final = cipher.decrypt(decode, None)
        if do_final is None:
            raise ValueError("Decryption failed!")

        b_arr:bytearray = bytearray()
        b_arr2:bytearray = bytearray()

        for i in range(0, 16):
            b_arr.insert(i, do_final[i])
        for i in range(0, 16):
            b_arr2.insert(i, do_final[i + 16])

        return TpLinkCipher(b_arr, b_arr2)

    @staticmethod
    def sha_digest_username(data: str):
        b_arr = data.encode("UTF-8")
        digest = hashlib.sha1(b_arr).digest()

        sb = ""
        for i in range(0, len(digest)):
            b = digest[i]
            hex_string = hex(b & 255).replace("0x", "")
            if len(hex_string) == 1:
                sb += "0"
                sb += hex_string
            else:
                sb += hex_string
        print(sb)
        return sb
