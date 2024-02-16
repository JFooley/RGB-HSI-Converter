from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import math
import cv2

def RGB_to_HSI(nome_da_imagem):
    imagem_rgb = Image.open(nome_da_imagem)

    # Defina as dimensões da imagem
    altura = imagem_rgb.height
    largura = imagem_rgb.width

    # Crie uma matriz vazia para armazenar os valores HSI
    imagem_hsi = np.zeros((altura, largura, 3), dtype=np.float32)

    # Abre o txt de output
    file = open("HSI.txt", "w")

    # Defina os valores de HSI para cada pixel
    for y in range(altura):
        for x in range(largura):
            pixel = imagem_rgb.getpixel((x, y))
            R = pixel[0]
            G = pixel[1]
            B = pixel[2]

            # Normaliza os valores de RGB
            R = R / 255
            G = G / 255
            B = B / 255

            # Calcula HSI
            teta = math.acos((R - G/2 - B/2) / math.sqrt(((R - G) * (R - G)) + (R - B) * (G - B)))
            teta = teta * (180.0 / math.pi)
            
            H = teta if B <= G else 360 - teta

            I = (R + G + B) / 3

            S = 0 if I == 0 else 1 - 3 / (R + G + B) * min(R, G, B)
            
            imagem_hsi[y, x] = [H, S, I]

            file.write(f"({x}, {x}) = H:{H:.2f} S:{S:.2f} I:{I:.2f}\n")

    file.close()
    
    return imagem_hsi

def HSI_to_RGB(imagem_hsi: str):
    altura = imagem_hsi.shape[0]
    largura = imagem_hsi.shape[1]

    # Crie uma matriz vazia para armazenar os valores HSI
    imagem_rgb = np.zeros((altura, largura, 3), dtype=np.float32)

    # Abre o txt de output
    file = open("RGB.txt", "w")

    for y in range(altura):
        for x in range(largura):
            H = imagem_hsi[y, x, 0]
            S = imagem_hsi[y, x, 1]
            I = imagem_hsi[y, x, 2]

            if H == 0:
                R = I + 2*I*S
                G = I - I*S
                B = I - I*S
            elif 0 < H and H < 120:
                R = I + I * S * math.cos(math.radians(H)) / math.cos(math.radians(60-H))
                G = I + I * S * (1 - math.cos(math.radians(H))/math.cos(math.radians(60-H)))
                B = I - I * S
            elif H == 120:
                R = I - I * S
                G = I + 2 * I * S
                B = I - I * S
            elif 120 < H and H < 240:
                R = I - I * S
                G = I + I * S * math.cos(math.radians(H-120)) / math.cos(math.radians(180-H))
                B = I + I * S * (1 - math.cos(math.radians(H-120)) / math.cos(math.radians(180-H)))
            elif H == 240:
                R = I - I * S
                G = I - I * S
                B = I + 2 * I * S
            elif 240 < H and H < 360:
                R = I + I * S * (1 - math.cos(math.radians(H-240)) / math.cos(math.radians(300-H)))
                G = I - I * S
                B = I + I * S * math.cos(math.radians(H-240)) / math.cos(math.radians(300-H))

            R = R * 255
            G = G * 255
            B = B * 255

            imagem_rgb[y, x] = [B, G, R]

            file.write(f"({x}, {x}) = R:{R:.2f} G:{G:.2f} B:{B:.2f}\n")
    
    file.close()

    return imagem_rgb

imagem_hsi = RGB_to_HSI("imagem.png")
imagem_bgr = HSI_to_RGB(imagem_hsi)

cv2.imwrite(f"nova_imagem.png", imagem_bgr)