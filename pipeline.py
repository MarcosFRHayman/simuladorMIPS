from analisador import Analisador
from csvBuffer import CSVBuffer
from instrucoes import NOP, Instrucao


class Pipeline:
    def __init__(self, buffer: CSVBuffer, analisador: Analisador) -> None:
        self.buffer = buffer
        self.analisador = analisador
        self.ID = NOP()
        self.IF = NOP()
        self.EX = NOP()
        self.MEM = NOP()
        self.WB = NOP()

    def avancaPipeline(self, instrucao: Instrucao):
        #trata variáveis
        self.WB = self.MEM
        self.MEM = self.EX
        self.EX = self.ID
        self.ID = self.IF
        self.IF = instrucao

        # Trata arquivo
        IF = self.buffer.getValorDaColuna("IF")
        ID = self.buffer.getValorDaColuna("ID")
        EX = self.buffer.getValorDaColuna("EX")
        MEM = self.buffer.getValorDaColuna("MEM")
        self.buffer.avancaCiclo()

        self.buffer.setValorDaColuna("WB", MEM)
        self.buffer.setValorDaColuna("MEM", EX)
        self.buffer.setValorDaColuna("EX", ID)
        self.buffer.setValorDaColuna("ID", IF)
        self.buffer.setValorDaColuna("IF", instrucao.gerarDescricao())
        self.buffer.setValorDaColuna("PC", 1)

    def executaAcoesDaPipeline(self):
        self.EX.EX()
        
