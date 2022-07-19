from csvBuffer import CSVBuffer

class MP:
    def __init__(self, buffer: CSVBuffer) -> None:
        self.buffer = buffer

    def getValorDaMemoria(self, id: int):
        return int(self.buffer.getValorDaColuna(id), 16)
    
    def setValorDaMemoria(self, id: int, valor: int):
        self.buffer.setValorDaColuna(id, hex(valor))
    
    def avancaCiclo(self):
        self.buffer.avancaCiclo(reseta_valores=False)