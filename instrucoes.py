class InstrucaoPrototipo:
    def __init__(self, pipeline, memoria, registradores) -> None:
        self.pipeline = pipeline
        self.memoria = memoria
        self.registradores = registradores

class Instrucao:
    def __init__(self, args, posicao, desc, prototipo: InstrucaoPrototipo) -> None:
        self.args = args
        self.posicao = posicao
        self.desc = desc
        self.prototipo = prototipo
    
    def IF(self):
        pass

    def ID(self):
        pass

    def EX(self):
        pass

    def MEM(self):
        pass

    def WB(self):
        pass
    
    def gerarDescricao(self) -> str:
        return self.desc

#========= SUB-CLASSES DE INSTRUÇÃO ===========
class NOP(Instrucao):
    def __init__(self) -> None:
        super().__init__(None, None, "NOP", None)

class TipoR(Instrucao):
    def __init__(self, args, posicao, comando, desc, prototipo) -> None:
        super().__init__(args, posicao, desc, prototipo)
        self.comando = comando

    def EX(self):
        super().EX()
        self.result = self.comando(self.args[1], self.args[2], self.args[2])
        print(self.result)


class TipoI(Instrucao):
    def __init__(self, args, posicao, comando, desc, prototipo) -> None:
        super().__init__(args, posicao, desc, prototipo)
        self.comando = comando

class TipoJ(Instrucao):
    def __init__(self, args, posicao, desc, prototipo) -> None:
        super().__init__(args, posicao, desc, prototipo)

class Branch(TipoI):
    def __init__(self, args, posicao, condicao, desc, prototipo) -> None:
        super().__init__(args, posicao, None, desc, prototipo)
        self.condicao = condicao

#========= GERADOR DE INSTRUÇÃO ===========


MAP_DE_INSTRUCOES = {
    "ADD": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x + y, desc, prototipo),
    "ADDI": lambda args, posicao, desc, prototipo: TipoI(args, posicao, lambda x, y, shamt: x + y, desc, prototipo),
    "AND": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x and y, desc, prototipo),
    "BEQ": lambda args, posicao, desc, prototipo: Branch(args, posicao, lambda x, y: x == y, desc, prototipo),
    "BNE": lambda args, posicao, desc, prototipo: Branch(args, posicao, lambda x, y: x != y, desc, prototipo),
    "J": lambda args, posicao, desc, prototipo: TipoJ(args, posicao, desc, prototipo),
    "JAL": lambda args, posicao, desc, prototipo: TipoJ(args, posicao, desc, prototipo),
    "JR": lambda args, posicao, desc, prototipo: TipoJ(args, posicao, desc, prototipo),
    "LW": lambda args, posicao, desc, prototipo: TipoI(args, posicao, None, desc, prototipo),
    "OR": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x or y, desc, prototipo),
    "SLL": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x * (2 ** shamt), desc, prototipo),
    "SRL": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x / (2 ** shamt), desc, prototipo),
    "SW": lambda args, posicao, desc, prototipo: TipoI(args, posicao, None, desc, prototipo),
    "SUB": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x - y, desc, prototipo),
    "NOP":  lambda args, posicao, desc, prototipo: NOP()
}

def geraInstrucao(nome: str, args, posicao, desc: str, prototipo) -> Instrucao:
    return MAP_DE_INSTRUCOES[nome](args, posicao, desc, prototipo)