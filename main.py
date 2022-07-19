from analisador import Analisador
from csvBuffer import CSVBuffer
from instrucoes import NOP, geraInstrucao
from pipeline import Pipeline


analisador = Analisador()
pipelineBuffer = CSVBuffer("resources/pipeline.csv", ["IF", "ID", "EX", "MEM", "WB", "PC"], "NOP" )
pipeline = Pipeline(pipelineBuffer, analisador)

registradores = ["$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3", "$t0", "$t1",
    "$t2", "$t3", "$t4", "$t5", "$t6", "$t7", "$s0", "$s1", "$s2", "$s3", "$s4",
    "$s5", "$s6","$s7", "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"]
registradoresBuffer = CSVBuffer("resources/registradores.csv", registradores, 0)

memoriaBuffer = CSVBuffer("resources/memoria.csv", [], 0)

nome_arquivo_asm = input("Digite o nome do arquivo de entrada:\n")
instrucoes = analisador.analisaArquivo(nome_arquivo_asm)
for instrucao  in instrucoes:
    pipeline.avancaPipeline(instrucao)
    pipeline.executaAcoesDaPipeline()
for i in range(4):
    pipeline.avancaPipeline(NOP())
    pipeline.executaAcoesDaPipeline()


pipelineBuffer.geraArquivo()
registradoresBuffer.geraArquivo()
memoriaBuffer.geraArquivo()
