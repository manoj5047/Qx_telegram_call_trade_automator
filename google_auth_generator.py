import base64
import hashlib
import hmac
import struct
import time

token = "ULTME6U2JF3B7YVV"

""" TOTP """
import hmac
import time


def totp(key: bytes):
    """ Calculate TOTP using time and key """
    now = int(time.time() // 30)
    msg = now.to_bytes(8, "big")
    digest = hmac.new(key, msg, "sha1").digest()
    offset = digest[19] & 0xF
    code = digest[offset : offset + 4]
    code = int.from_bytes(code, "big") & 0x7FFFFFFF
    code = code % 1000000
    return "{:06d}".format(code)
# def get_hotp_token(secret, intervals_no):
#     key = base64.b32decode(secret, True)
#     msg = struct.pack(">Q", intervals_no)
#     h = hmac.new(key, msg, hashlib.sha1).digest()
#     o = ord(h[19]) & 15
#     h = (struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000
#     return h
#
#
# def get_totp_token(secret):
#     return get_hotp_token(secret=token, intervals_no=int(time.time()) // 30)


# print(str(get_totp_token(secret=token)))
print(str(totp(key=token.ge)))
