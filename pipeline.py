from analisador import Analisador
from csvBuffer import CSVBuffer
from instrucoes import NOP, Instrucao


class Pipeline:
    def __init__(self, buffer: CSVBuffer) -> None:
        self.buffer = buffer
        self.analisador = None

    def setAnalisador(self, analisador: Analisador):
        self.analisador = analisador
        self.ID = NOP("NOP", analisador.prototipo)
        self.IF = NOP("NOP", analisador.prototipo)
        self.EX = NOP("NOP", analisador.prototipo)
        self.MEM = NOP("NOP", analisador.prototipo)
        self.WB = NOP("NOP", analisador.prototipo)

    def avancaPipeline(self, instrucao: Instrucao):
        #trata variáveis
        self.WB = self.MEM
        self.MEM = self.EX
        self.EX = self.ID
        self.ID = self.IF
        self.IF = instrucao

        # Trata arquivo csv
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

    def executaAcoesDaPipeline(self):
        self.IF.IF()
        self.ID.ID()
        self.EX.EX()
        self.MEM.MEM()
        self.WB.WB()

        
