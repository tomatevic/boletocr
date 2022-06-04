from typing import BinaryIO


import boto3
import variables
import pdf2image
import json
import re

textract = boto3.client('textract', region_name="us-east-1")


class Boleto:
    agenciaCodigoBeneficiario: str
    beneficiario: str
    codigo: str
    dataDoDocumento: str
    desconto: str
    multa: str
    nossoNumero: str
    pagador: str
    valor: str
    vencimento: str


class Boletocr:
    boleto: dict
    sucesso: bool
    mensagem: str

    def successResponse(self):
        self.sucesso = True
        return self

    def errorResponse(self, error: str):
        self.sucesso = False
        self.mensagem = error
        return self


def readBoleto(file: BinaryIO):
    response = Boletocr()
    try:
        codigo = __validateDocumentAndReturnCodigo(file)
        __pdfToImage(file)
        textractresponse = __callTextract()
        boletoresponse = __filterResponse(textractresponse)
        boletoresponse.codigo = codigo

        response.boleto = boletoresponse.__dict__

        return json.dumps(response.successResponse().__dict__)
    except Exception as e:
        return json.dumps(Boletocr().errorResponse(e.__str__()).__dict__)


def __validateDocumentAndReturnCodigo(file: BinaryIO):
    if not file.name.endswith('.pdf'):
        raise Exception('Formato de arquivo precisa ser em PDF.')

    with open(variables.imgboleto, 'rb') as image:
        response = textract.detect_document_text(
            Document={
                'Bytes': image.read()
            }
        )
        blocks = response['Blocks']
        for block in blocks:
            if block['BlockType'] != 'PAGE':
                text = str(block['Text']).translate({ord(ch): '' for ch in ' .'})
                a = re.match("([0-9]{46,})", text)
                if a:
                    return a.string

    raise Exception("O arquivo precisa ser um boleto")

def __pdfToImage(file: BinaryIO):
    image = pdf2image.convert_from_bytes(file.read(), poppler_path=variables.poppler)

    image[0].save(variables.imgboleto, 'JPEG')



def __callTextract():
    with open(variables.imgboleto, 'rb') as image:
        response = textract.analyze_expense(
            Document={
                'Bytes': image.read()
            }
        )

        return response


def __filterResponse(textractResponse):
    boleto = Boleto()
    boleto.agenciaCodigoBeneficiario = __findValueByLabel(variables.agenciaCodigo, textractResponse)
    boleto.beneficiario = __findValueByLabel(variables.beneficiario, textractResponse)
    boleto.dataDoDocumento = __findValueByLabel(variables.data_do_documento, textractResponse)
    boleto.desconto = __findValueByLabel(variables.desconto, textractResponse)
    boleto.multa = __findValueByLabel(variables.multa, textractResponse)
    boleto.nossoNumero = __findValueByLabel(variables.nosso_numero, textractResponse)
    boleto.pagador = __findValueByLabel(variables.pagador, textractResponse)
    boleto.valor = __findValueByLabel(variables.valor, textractResponse)
    boleto.vencimento = __findValueByLabel(variables.vencimento, textractResponse)

    return boleto


def __findValueByLabel(label: str, txtctresponse):
    for expense_doc in txtctresponse["ExpenseDocuments"]:
        for field in expense_doc["SummaryFields"]:
            if "LabelDetection" not in field:
                continue

            key = field.get("LabelDetection")["Text"].lower().translate({ord(ch): '' for ch in ' (=)'})

            if key.startswith(label):
                value = field.get("ValueDetection")["Text"].lower()

                if value:
                    return value

    return None
