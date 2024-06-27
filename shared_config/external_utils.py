import binascii
import json
import string
import random
import base64
from datetime import date, datetime
from . import settings
from .external_constants import AES_BLOCK_SIZE, AES_SEGMENT_SIZE, AES_PAD_VALUE
from Crypto.Cipher import AES

def encrypt_response_json(request, encrypted_response_data):
    """
    Function to encrypt the complete json response
    :param request: request object used for logging.
    :param encrypted_response_data: A dictionary object which needs to be encrypted.
    :return: Encrypted response
    """

    if encrypted_response_data:
        encrypt_object = EncryptionDecryption()
        value = json.dumps(encrypted_response_data, default=json_serial)
        return encrypt_object.encrypt_value(value)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
   
class EncryptionDecryption:
    """
    Class for Encryption and Decryption. It creates the object of AESEncrypterDecrypter class and calls their
    encryption and decryption function.
    """

    def encrypt_value(self, value):
        """
        This function calls the AES encryption function and returns the encrypted string.
        :param value: string which needs to be encrypted.
        :return: encrypted String.
        """
        iv = "".join(random.sample(string.ascii_letters, 16)).encode('utf-8')
        key = "".join(random.sample(string.ascii_letters, 32)).encode('utf-8')
        s = AESEncrypterDecrypter(key, iv)
        encrypted_value = s.encrypt(value)
        print(encrypted_value)
        return base64.b64encode(iv + encrypted_value + key).decode("utf-8")
    
class AESEncrypterDecrypter:
    """
    A class that performs the actual AES encryption and decryption.
    """
    def __init__(self, key=None, iv=None):
        """
        Constructor to set the default data such as key, mode etc to a object.
        """
        self.KEY = key if key else settings.AES_KEY.encode('utf-8')
        self.IV = iv if iv else settings.AES_IV.encode('utf-8')
        self.MODE = AES.MODE_CFB
        self.BLOCK_SIZE = AES_BLOCK_SIZE
        self.SEGMENT_SIZE = AES_SEGMENT_SIZE

    def _pad_string(self, value):
        """
        A class method which is used for padding the string received, as AES encrypts the data block by block,
        so padding is done if value is smaller than a block size.
        :param value: string which needs to be padded.
        :return: padded string
        """
        length = len(value)
        pad_size = self.BLOCK_SIZE - (length % self.BLOCK_SIZE)
        return value.ljust(length + pad_size, AES_PAD_VALUE)
    
    def encrypt(self, plaintext):
        """
        A class method which receives plaintext and performs AES encryption on it.
        :param plaintext: Plaintext to be encrypted.
        :return: Encrypted byte string.
        """
        aes = AES.new(self.KEY, self.MODE, self.IV, segment_size=self.SEGMENT_SIZE)
        plaintext = self._pad_string(plaintext)
        encrypted_text = aes.encrypt(plaintext.encode('utf-8'))
        return binascii.b2a_hex(encrypted_text).rstrip()