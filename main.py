from csv import DictWriter
from csvBuffer import CSVBuffer


pipelineBuffer = CSVBuffer("pipeline.csv", ["ID", "IF", "EX", "MEM", "WB"], "NOP" )

registradoresBuffer = CSVBuffer(
    "registradores.csv",
    ["$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3", "$t0", "$t1",
    "$t2", "$t3", "$t4", "$t5", "$t6", "$t7", "$s0", "$s1", "$s2", "$s3", "$s4",
    "$s5", "$s6","$s7", "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"],
    0)

memoriaBuffer = CSVBuffer("memoria.csv", [], 0)

pipelineBuffer.generateFile()
registradoresBuffer.generateFile()
memoriaBuffer.generateFile()


# with open("registradores.csv", "w") as csvfile:
#     writer = DictWriter(csvfile, 
#         ["ciclo", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3", "$t0", "$t1",
#         "$t2", "$t3", "$t4", "$t5", "$t6", "$t7", "$s0", "$s1", "$s2", "$s3", "$s4",
#          "$s5", "$s6","$s7", "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"])
#     writer.writeheader()

# with open("memoria.csv", "w") as csvfile:
#     writer = DictWriter(csvfile, 
#         ["ciclo", ""])
#     writer.writeheader()
    
