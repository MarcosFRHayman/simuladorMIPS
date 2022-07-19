from mp import MP
from registradores import Registradores


class InstrucaoPrototipo:
    def __init__(self, pipeline, memoria: MP, registradores: Registradores) -> None:
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
        registradores = self.prototipo.registradores
        pc = registradores.getValorDoRegistrador("PC")
        registradores.setValorDoRegistrador("PC", pc + 4)

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
    def __init__(self, prototipo) -> None:
        super().__init__(None, None, "NOP", prototipo)
        

class TipoR(Instrucao):
    def __init__(self, args, posicao, comando, desc, prototipo) -> None:
        super().__init__(args, posicao, desc, prototipo)
        self.comando = comando

    def EX(self):
        super().EX()
        rs = self.prototipo.registradores.getValorDoRegistrador(self.args[1])
        rd = self.prototipo.registradores.getValorDoRegistrador(self.args[2])
        shamt = None
        try:
            shamt = int(self.args[2])
        except ValueError:
            pass
        if self.comando != None:
            self.result = self.comando(rs, rd, shamt)
            print(self.result)
    
    def WB(self):
        super().WB()
        self.prototipo.registradores.setValorDoRegistrador(self.args[0], self.result)


class TipoI(Instrucao):
    def __init__(self, args, posicao, comando, desc, prototipo) -> None:
        super().__init__(args, posicao, desc, prototipo)
        self.comando = comando
    
    def EX(self):
        super().EX()
        rs = self.prototipo.registradores.getValorDoRegistrador(self.args[1])
        if self.comando != None:
            self.result = self.comando(rs, int(self.args[2]), int(self.args[2]))
            print(self.result)
    
    def WB(self):
        super().WB()
        self.prototipo.registradores.setValorDoRegistrador(self.args[0], self.result)

class TipoJ(Instrucao):
    def __init__(self, args, posicao, desc, prototipo) -> None:
        super().__init__(args, posicao, desc, prototipo)

class Branch(TipoI):
    def __init__(self, args, posicao, condicao, desc, prototipo) -> None:
        super().__init__(args, posicao, None, desc, prototipo)
        self.condicao = condicao

class LW(TipoI):
    def __init__(self, args, posicao, desc, prototipo) -> None:
        super().__init__(args, posicao, None, desc, prototipo)
    
    def EX(self):
        self.endereco = self.calculaEndereco(self.args[1])

    def MEM(self):
        super().MEM()
        self.valorDaMemoria = self.prototipo.memoria.getValorDaMemoria(self.endereco)
    
    def WB(self):
        self.prototipo.registradores.setValorDoRegistrador(self.args[0], self.valorDaMemoria)

    def calculaEndereco(self, arg: str):
        imediato, reg = arg.split("(")
        #remove o fecha parenteses
        reg = reg[:-1]
        return int(imediato) + self.prototipo.registradores.getValorDoRegistrador(reg)

class SW(TipoI):
    def __init__(self, args, posicao, desc, prototipo) -> None:
        super().__init__(args, posicao, None, desc, prototipo)

    def EX(self):
        self.endereco = self.calculaEndereco(self.args[1])
        self.reg = self.prototipo.registradores.getValorDoRegistrador(self.args[0])
    
    def MEM(self):
        super().MEM()
        self.prototipo.memoria.setValorDaMemoria(self.endereco, self.reg)
    
    def WB(self):
        pass

    def calculaEndereco(self, arg: str):
        imediato, reg = arg.split("(")
        #remove o fecha parenteses
        reg = reg[:-1]
        return int(imediato) + self.prototipo.registradores.getValorDoRegistrador(reg)


#========= GERADOR DE INSTRUÇÃO ===========


MAP_DE_INSTRUCOES = {
    "ADD": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x + y, desc, prototipo),
    "ADDI": lambda args, posicao, desc, prototipo: TipoI(args, posicao, lambda x, y, shamt: x + y, desc, prototipo),
    "AND": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x & y, desc, prototipo),
    "BEQ": lambda args, posicao, desc, prototipo: Branch(args, posicao, lambda x, y: x == y, desc, prototipo),
    "BNE": lambda args, posicao, desc, prototipo: Branch(args, posicao, lambda x, y: x != y, desc, prototipo),
    "J": lambda args, posicao, desc, prototipo: TipoJ(args, posicao, desc, prototipo),
    "JAL": lambda args, posicao, desc, prototipo: TipoJ(args, posicao, desc, prototipo),
    "JR": lambda args, posicao, desc, prototipo: TipoJ(args, posicao, desc, prototipo),
    "LW": lambda args, posicao, desc, prototipo: LW(args, posicao, desc, prototipo),
    "OR": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x | y, desc, prototipo),
    "SLL": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x * (2 ** shamt), desc, prototipo),
    "SRL": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x / (2 ** shamt), desc, prototipo),
    "SW": lambda args, posicao, desc, prototipo: SW(args, posicao, desc, prototipo),
    "SUB": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x - y, desc, prototipo),
    "NOP":  lambda args, posicao, desc, prototipo: NOP(prototipo)
}

def geraInstrucao(nome: str, args, posicao, desc: str, prototipo) -> Instrucao:
    return MAP_DE_INSTRUCOES[nome](args, posicao, desc, prototipo)