""" Различные полезные функции """
import hashlib

def create_md5(p_line, p_salt):

    if p_salt is not None:

        return hashlib.md5(bytes(p_line+p_salt, "ANSI")).hexdigest()
    else:
        return hashlib.md5(bytes(p_line, "ANSI")).hexdigest()
