import boletocr

file = open('imagem.png', 'rb')
response = boletocr.readBoleto(file)
print(response)

file2 = open('invalidPDF.pdf', 'rb')
response = boletocr.readBoleto(file2)
print(response)

file3 = open('boleto.pdf', 'rb')
response = boletocr.readBoleto(file3)
print(response)

