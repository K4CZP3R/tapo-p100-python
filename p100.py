import jsons
from encryption import Encryption
from logger import Logger
from models.key_pair import KeyPair
from models.params.handshake_params import HandshakeParams
from models.methods.login_device_method import LoginDeviceMethod
from models.params.login_device_params import LoginDeviceParams
from models.methods.handshake_method import HandshakeMethod
from models.methods.device_info_method import DeviceInfoMethod
from models.params.device_info_params import DeviceInfoParams
from models.methods.secure_passthrough_method import SecurePassthroughMethod
from http_client import Http
from models.exceptions.ResponseErrorCodeNotZero import ResponseErrorCodeNotZero
from time import time
from tp_link_cipher import TpLinkCipher
import helpers


class P100:
    def __init__(self, address: str):
        self.address = address
        self.url = f"http://{address}/app"

        self.encryption = Encryption()
        self.log = Logger("P100")

        self.key_pair: KeyPair
        self.cookie_token: str = ""
        self.token: str = ""

        self.tp_link_cipher: TpLinkCipher = None

    def change_state(self, new_state: bool, terminal_uuid: str):
        device_info_params = DeviceInfoParams()
        device_info_params.set_device_on(new_state)

        device_info_method = DeviceInfoMethod(device_info_params)
        device_info_method.set_request_time_milis(time())
        device_info_method.set_terminal_uuid(terminal_uuid)
        self.log.out(jsons.dumps(device_info_method))
        dim_encrypted = self.tp_link_cipher.encrypt(jsons.dumps(device_info_method))

        secure_passthrough_method = SecurePassthroughMethod(dim_encrypted)
        request_body = jsons.loads(jsons.dumps(secure_passthrough_method))

        self.log.out(f"request_body: {request_body}")

        response = Http.make_post_cookie(f"{self.url}?token={self.token}", request_body,
                                         {'TP_SESSIONID':self.cookie_token})
        resp_dict: dict = response.json()

        self.__validate_response(resp_dict)
        self.log.out(f"response: {resp_dict}")
        self.log.out(f"{self.tp_link_cipher.decrypt(resp_dict['result']['response'])}")



    def handshake(self):
        self.log.out("Generating keypair...")
        self.__generate_keypair()
        self.log.out(f"Public key: {self.key_pair.get_public_key()}")

        handshake_params = HandshakeParams()
        handshake_params.set_key(self.key_pair.get_public_key())

        handshake_method = HandshakeMethod(handshake_params)

        request_body = jsons.dump(handshake_method)
        self.log.out(f"request_body: {request_body}")

        response = Http.make_post(self.url, request_body)
        resp_dict: dict = response.json()

        self.__validate_response(resp_dict)

        self.log.out(f"response: {resp_dict}")
        self.log.out(f"cookies: {response.cookies.get('TP_SESSIONID')}")

        self.cookie_token = response.cookies.get('TP_SESSIONID')

        self.tp_link_cipher = self.encryption.decode_handshake_key(resp_dict['result']['key'], self.key_pair)

    def login_request(self, username: str, password: str) -> bool:
        digest_username = self.encryption.sha_digest_username(username)

        login_device_params = LoginDeviceParams()
        login_device_params.set_password(helpers.mime_encoder(password.encode("UTF-8")))
        login_device_params.set_username(helpers.mime_encoder(digest_username.encode("UTF-8")))

        login_device_method = LoginDeviceMethod(login_device_params)
        self.log.out(f"unencrypted: {jsons.dumps(login_device_method)}")

        ldm_encrypted = self.tp_link_cipher.encrypt(jsons.dumps(login_device_method))

        secure_passthrough_method = SecurePassthroughMethod(ldm_encrypted)
        request_body = jsons.loads(jsons.dumps(secure_passthrough_method))
        self.log.out(f"request_body: {request_body}")

        response = Http.make_post_cookie(self.url, request_body, {'TP_SESSIONID':self.cookie_token})
        resp_dict: dict = response.json()

        self.__validate_response(resp_dict)
        self.log.out(f"response: {resp_dict}")

        decrypted = jsons.loads(self.tp_link_cipher.decrypt(resp_dict['result']['response']))
        print(decrypted)
        self.token = decrypted['result']['token']
        return True

    def __generate_keypair(self):
        self.key_pair = self.encryption.generate_key_pair()

    def __validate_response(self, resp: dict):
        if 'error_code' not in resp:
            self.log.out("WARN: No error_code in the response!")
        else:
            if resp['error_code'] != 0:
                raise ResponseErrorCodeNotZero(f"Returned error_code: {resp['error_code']}")
