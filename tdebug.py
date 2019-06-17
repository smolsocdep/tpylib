import constants as const

def dout(*params):
    if const.__DEBUG__:
        print(params)
