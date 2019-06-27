# from itsdangerous import Signer
from itsdangerous import URLSafeTimedSerializer


# s = Signer("secret-key")
# signature = JSONWebSignatureSerializer('secret-key')
serializer = URLSafeTimedSerializer('secret-key')
