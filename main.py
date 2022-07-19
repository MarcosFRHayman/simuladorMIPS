from cmath import e
from analisador import Analisador
from csvBuffer import CSVBuffer
from instrucoes import NOP, InstrucaoPrototipo, geraInstrucao
from mp import MP
from pipeline import Pipeline
from registradores import Registradores


analisador = Analisador()
 
# Inicia Pipeline
pipelineBuffer = CSVBuffer("resources/pipeline.csv", ["IF", "ID", "EX", "MEM", "WB"], "NOP" )
pipeline = Pipeline(pipelineBuffer)

#Inicia Registradores
registradores = ["pc", "$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3", "$t0", "$t1",
    "$t2", "$t3", "$t4", "$t5", "$t6", "$t7", "$s0", "$s1", "$s2", "$s3", "$s4",
    "$s5", "$s6","$s7", "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"]
registradoresBuffer = CSVBuffer("resources/registradores.csv", registradores, 0)
bancoDeRegistradores = Registradores(registradoresBuffer)

#Inicia MP
memoriaBuffer = CSVBuffer("resources/memoria.csv", list(range(1000)), hex(0))
mp = MP(memoriaBuffer)

analisador.setPrototipo(InstrucaoPrototipo(pipeline, mp, bancoDeRegistradores))
pipeline.setAnalisador(analisador)

# nome_arquivo_asm = input("Digite o nome do arquivo de entrada:\n")
nome_arquivo_asm = "resources/teste"
instrucoes = analisador.analisaArquivo(nome_arquivo_asm)

pc = bancoDeRegistradores.getValorDoRegistrador("PC")
while (pc / 4 < len(instrucoes)):
        instrucao = instrucoes[int(pc/4)]
        pipeline.avancaPipeline(instrucao)
        pipeline.executaAcoesDaPipeline()
        # pc = bancoDeRegistradores.getValorDoRegistrador("PC")
        # try:
        # except IndexError:
        #     instrucao = NOP("NOP", analisador.prototipo)
        bancoDeRegistradores.avancaCiclo()
        mp.avancaCiclo()
        pc = bancoDeRegistradores.getValorDoRegistrador("PC")


for i in range(4):
    pipeline.executaAcoesDaPipeline()
    pipeline.avancaPipeline(NOP("NOP", analisador.prototipo))
    bancoDeRegistradores.avancaCiclo()
    mp.avancaCiclo()
pipeline.executaAcoesDaPipeline()


pipelineBuffer.geraArquivo()
registradoresBuffer.geraArquivo()
memoriaBuffer.geraArquivo()
