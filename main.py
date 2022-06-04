import boletocr

file = open('boleto.pdf', 'rb')

response = boletocr.readBoleto(file)
print(response)

