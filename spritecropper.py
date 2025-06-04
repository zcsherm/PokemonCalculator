from PIL import Image

#mon = input("Which Pokemon?").lower()
def crop(mon):
    front = Image.open(r"C:/Users/zashe/code/PokemonASM/Decomp pure backup/decomps/pokeemerald/{}front.bmp".format(mon))
    back = Image.open(r"C:/Users/zashe/code/PokemonASM/Decomp pure backup/decomps/pokeemerald/{}back.bmp".format(mon))
    pathtodecomp = f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{mon}"
    width, height  =front.size
    if width == 64 and height == 128:
        front.save(f"{pathtodecomp}/anim_front.png")
        af = True
    else:
        print(f"anim_front.png is not expected size. Please check source file.\nEXPECTED: 64x128 --- RECEIVED: {width}x{height}")
    still = front.crop((0,0,width,height/2))
    width, height = still.size
    if width == 64 and height == 64:
        still.save(f"{pathtodecomp}/front.png")
        f = True
    else:
        print(f"front.png is not expected size. Please check source file.\nEXPECTED: 64x64 --- RECEIVED: {width}x{height}")
    width, height = back.size
    if width == 64 and height == 64:
        back.save(f"{pathtodecomp}/back.png")
        b = True
    else:
        print(f"back.png is not expected size. Please check source file.\nEXPECTED: 64x64 --- RECEIVED: {width}x{height}")
    print("===================FILE DETAILS========================")
    if af:
        print(f"Successfully saved anim_front.png to {pathtodecomp}/anim_front.png")
    else:
        print("FAILURE Failed to save anim_front.png")
    if f:
        print(f"Successfully saved front.png to {pathtodecomp}/front.png")
    else:
        print("FAILURE Failed to save front.png")
    if b:
        print(f"Successfully saved back.png to {pathtodecomp}/back.png")
    else:
        print("FAILURE Failed to save back.png")
