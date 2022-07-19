from mp import MP
from registradores import Registradores


class InstrucaoPrototipo:
    def __init__(self, pipeline, memoria: MP, registradores: Registradores) -> None:
        self.pipeline = pipeline
        self.memoria = memoria
        self.registradores = registradores
    
    def setAnalisador(self, analisador):
        self.analisador = analisador

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
    def __init__(self, desc, prototipo) -> None:
        super().__init__(None, None, desc, prototipo)
        

class TipoR(Instrucao):
    def __init__(self, args, posicao, comando, desc, prototipo) -> None:
        super().__init__(args, posicao, desc, prototipo)
        self.comando = comando

    def EX(self):
        super().EX()
        rs = self.prototipo.registradores.getValorDoRegistrador(self.args[1])
        rd = None
        shamt = None
        try:
            shamt = int(self.args[2])
        except ValueError:
            rd = self.prototipo.registradores.getValorDoRegistrador(self.args[2])
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
        rs = self.prototipo.registradores.getValorDoRegistrador(self.args[1])
        if self.comando != None:
            self.result = self.comando(rs, int(self.args[2]), int(self.args[2]))
            print(self.result)
    
    def WB(self):
        self.prototipo.registradores.setValorDoRegistrador(self.args[0], self.result)

class TipoJ(Instrucao):
    def __init__(self, args, posicao, desc, prototipo) -> None:
        super().__init__(args, posicao, desc, prototipo)
    
    def ID(self):
        super().ID()
        enderecoAlvo = self.args[0]
        if (type(enderecoAlvo) is int):
            enderecoAlvo = enderecoAlvo * 4
        elif(type(enderecoAlvo) is str):
            enderecoAlvo = self.prototipo.analisador.getEnderecoDeLabel(enderecoAlvo.upper().strip())
            enderecoAlvo = int(enderecoAlvo) * 4
        self.prototipo.registradores.setValorDoRegistrador("PC", enderecoAlvo)
        


class LW(TipoI):
    def __init__(self, args, posicao, desc, prototipo) -> None:
        super().__init__(args, posicao, None, desc, prototipo)
    
    def EX(self):
        self.endereco = self.calculaEndereco(self.args[1])

    def MEM(self):
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
        self.prototipo.memoria.setValorDaMemoria(self.endereco, self.reg)
    
    def WB(self):
        pass

    def calculaEndereco(self, arg: str):
        imediato, reg = arg.split("(")
        #remove o fecha parenteses
        reg = reg[:-1]
        return int(imediato) + self.prototipo.registradores.getValorDoRegistrador(reg)

class Branch(TipoI):
    def __init__(self, args, posicao, condicao, desc, prototipo) -> None:
        super().__init__(args, posicao, None, desc, prototipo)
        self.condicao = condicao
    
    def ID(self):
        super().ID()
        registradores = self.prototipo.registradores
        rs = registradores.getValorDoRegistrador(self.args[0])
        rt = registradores.getValorDoRegistrador(self.args[1])
        enderecoAlvo = self.args[2]
        if (type(enderecoAlvo) is int):
            enderecoAlvo = enderecoAlvo * 4
        elif(type(enderecoAlvo) is str):
            enderecoAlvo = self.prototipo.analisador.getEnderecoDeLabel(enderecoAlvo.upper().strip())
            enderecoAlvo = int(enderecoAlvo) * 4
        if self.condicao(rs, rt):
            registradores.setValorDoRegistrador("PC", enderecoAlvo)
    
    def EX(self):
        pass
    def WB(self):
        pass

class JAL(TipoJ):
    def __init__(self, args, posicao, desc, prototipo) -> None:
        super().__init__(args, posicao, desc, prototipo)
    
    def WB(self):
        self.prototipo.registradores.setValorDoRegistrador("$ra", self.posicao + 1)

class JR(TipoJ):
    def __init__(self, args, posicao, desc, prototipo) -> None:
        super().__init__(args, posicao, desc, prototipo)
    
    def ID(self):
        enderecoAlvo = self.args[0]
        enderecoAlvo = self.prototipo.registradores.getValorDoRegistrador(enderecoAlvo)
        enderecoAlvo = int(enderecoAlvo) * 4
        self.prototipo.registradores.setValorDoRegistrador("PC", enderecoAlvo)



#========= GERADOR DE INSTRUÇÃO ===========


MAP_DE_INSTRUCOES = {
    "ADD": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x + y, desc, prototipo),
    "ADDI": lambda args, posicao, desc, prototipo: TipoI(args, posicao, lambda x, y, shamt: x + y, desc, prototipo),
    "AND": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x & y, desc, prototipo),
    "BEQ": lambda args, posicao, desc, prototipo: Branch(args, posicao, lambda x, y: x == y, desc, prototipo),
    "BNE": lambda args, posicao, desc, prototipo: Branch(args, posicao, lambda x, y: x != y, desc, prototipo),
    "J": lambda args, posicao, desc, prototipo: TipoJ(args, posicao, desc, prototipo),
    "JAL": lambda args, posicao, desc, prototipo: JAL(args, posicao, desc, prototipo),
    "JR": lambda args, posicao, desc, prototipo: JR(args, posicao, desc, prototipo),
    "LW": lambda args, posicao, desc, prototipo: LW(args, posicao, desc, prototipo),
    "OR": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x | y, desc, prototipo),
    "SLL": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x * (2 ** shamt), desc, prototipo),
    "SRL": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x / (2 ** shamt), desc, prototipo),
    "SW": lambda args, posicao, desc, prototipo: SW(args, posicao, desc, prototipo),
    "SUB": lambda args, posicao, desc, prototipo: TipoR(args, posicao, lambda x, y, shamt: x - y, desc, prototipo),
    "NOP":  lambda args, posicao, desc, prototipo: NOP(desc, prototipo)
}

def geraInstrucao(nome: str, args, posicao, desc: str, prototipo) -> Instrucao:
    return MAP_DE_INSTRUCOES[nome](args, posicao, desc, prototipo)