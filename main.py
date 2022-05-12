import boletocr

file = open('boleto.pdf', 'rb')

boletocr.readBoleto(file)

