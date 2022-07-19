from analisador import Analisador
from csvBuffer import CSVBuffer
from instrucoes import NOP, InstrucaoPrototipo, geraInstrucao
from mp import MP
from pipeline import Pipeline
from registradores import Registradores


analisador = Analisador()

# Inicia Pipeline
pipelineBuffer = CSVBuffer("resources/pipeline.csv", ["IF", "ID", "EX", "MEM", "WB"], "NOP" )
pipeline = Pipeline(pipelineBuffer, analisador)

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

# nome_arquivo_asm = input("Digite o nome do arquivo de entrada:\n")
nome_arquivo_asm = "resources/teste"
instrucoes = analisador.analisaArquivo(nome_arquivo_asm)
for instrucao in instrucoes:
    pipeline.executaAcoesDaPipeline()
    pipeline.avancaPipeline(instrucao)
    bancoDeRegistradores.avancaCiclo()
    mp.avancaCiclo()

for i in range(4):
    pipeline.executaAcoesDaPipeline()
    pipeline.avancaPipeline(NOP())
    bancoDeRegistradores.avancaCiclo()
    mp.avancaCiclo()


pipelineBuffer.geraArquivo()
registradoresBuffer.geraArquivo()
memoriaBuffer.geraArquivo()
