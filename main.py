import boletocr
import os
import time


for filename in os.listdir(os.path.join(os.getcwd(), "arquivos")):
    print("--- Iniciando execução: %s ---" % filename)
    tempo = time.time()
    with open(os.path.join(os.getcwd(), "arquivos", filename), 'rb') as f:
        response = boletocr.readBoleto(f)
        print(response)
        print("--- Executado em %s segundos ---" % (time.time() - tempo))
        print()

