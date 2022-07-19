from csvBuffer import CSVBuffer

class Registradores:
    def __init__(self, buffer: CSVBuffer) -> None:
        self.buffer = buffer
    
    def getValorDoRegistrador(self, id: str):
        id = id.lower().strip()
        return int(self.buffer.getValorDaColuna(id))
    
    def setValorDoRegistrador(self, id: str, valor):
        id = id.lower().strip()
        self.buffer.setValorDaColuna(id, valor)
    
    def avancaCiclo(self):
        self.buffer.avancaCiclo(reseta_valores=False)
