from os.path import isdir
from analisador import Analisador
from csvBuffer import CSVBuffer
from instrucoes import NOP, InstrucaoPrototipo, ReadonlyRegisterException, geraInstrucao
from mp import MP
from pipeline import Pipeline
from registradores import Registradores

nome_arquivo_asm = input("Digite o nome do arquivo de entrada:\n")
pasta_valida = False
while not pasta_valida:
    pasta_resultado = input("Digite em qual pasta deseja salvar os resultados:\n")
    pasta_valida = isdir(pasta_resultado)
    if not pasta_valida:
        print("\nEssa pasta não existe\n")

analisador = Analisador()
 
# Inicia Pipeline
pipelineBuffer = CSVBuffer(f"{pasta_resultado}/pipeline.csv", ["IF", "ID", "EX", "MEM", "WB"], "NOP" )
pipeline = Pipeline(pipelineBuffer)

#Inicia Registradores
registradores = ["pc", "$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3", "$t0", "$t1",
    "$t2", "$t3", "$t4", "$t5", "$t6", "$t7", "$s0", "$s1", "$s2", "$s3", "$s4",
    "$s5", "$s6","$s7", "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"]
registradoresBuffer = CSVBuffer(f"{pasta_resultado}/registradores.csv", registradores, 0)
bancoDeRegistradores = Registradores(registradoresBuffer)

#Inicia MP
memoriaBuffer = CSVBuffer(f"{pasta_resultado}/memoria.csv", list(range(0, 4000, 4)), hex(0))
mp = MP(memoriaBuffer)

analisador.setPrototipo(InstrucaoPrototipo(pipeline, mp, bancoDeRegistradores))
pipeline.setAnalisador(analisador)

instrucoes = analisador.analisaArquivo(nome_arquivo_asm)

pc = bancoDeRegistradores.getValorDoRegistrador("PC")

try:
    while (pc / 4 < len(instrucoes) or ultima_instrucao < 4):
        if pc / 4 < len(instrucoes):
            instrucao = instrucoes[int(pc/4)]
            ultima_instrucao = 0
        else:
            instrucao = (NOP("NOP", analisador.prototipo))
            ultima_instrucao += 1
        pipeline.avancaPipeline(instrucao)
        bancoDeRegistradores.avancaCiclo()
        mp.avancaCiclo()
        pipeline.executaAcoesDaPipeline()
        pc = bancoDeRegistradores.getValorDoRegistrador("PC")

    print("Simulação bem sucedida!")
# except ReadonlyRegisterException:
#     raise ReadonlyRegisterException().with_traceback()
finally:
    pipelineBuffer.geraArquivo()
    registradoresBuffer.geraArquivo()
    memoriaBuffer.geraArquivo()