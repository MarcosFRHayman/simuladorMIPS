from instrucoes import Instrucao, geraInstrucao

class Analisador:
    def __init__(self) -> None:
        self.map_de_label = {}
        self.prototipo = None

    def setPrototipo(self, prototipo):
        self.prototipo = prototipo

    def avaliaLabels(self, nome_arquivo_asm) -> list:
        map_de_label = {}
        with open(f'{nome_arquivo_asm}.asm', 'r') as arquivo_asm:
            linhas = arquivo_asm.readlines()
            for zipper in zip(linhas, range(len(linhas))):
                linha, i = zipper
                split_label = linha.split(": ")
                #Se tem mais de um então o padrão foi encontrado, logo há uma label na posição
                if len(split_label) > 1:
                    map_de_label[split_label[0]] = i
        return map_de_label

    def analisaArquivo(self, nome_arquivo_asm) -> list:
        construtores_de_instrucao = []
        with open(f'{nome_arquivo_asm}.asm', 'r') as arquivo_asm:
            linhas = arquivo_asm.readlines()
            for zipper in zip(linhas, range(len(linhas))):
                linha, i = zipper
                split_label = linha.split(": ")
                #Se tem mais de um então o padrão foi encontrado, logo há uma label na posição
                if len(split_label) > 1:
                    self.map_de_label[split_label[0]] = i
                construtores_de_instrucao.append(self.analisaLinha(linha.strip(), i))
        return construtores_de_instrucao

    def analisaLinha(self, linha: str, i) -> Instrucao:
        linha_sem_label = linha.split(": ")[-1]

        separacao = linha_sem_label.split(",")
        try:
            id_instrucao, primeiro_argumento = separacao[0].split(" ")
            argumentos = [primeiro_argumento] + separacao[1:]
            return geraInstrucao(id_instrucao, argumentos, i + 1, linha, self.prototipo)
        except ValueError:
            return geraInstrucao(separacao[0], None, i + 1, separacao[0], self.prototipo)
