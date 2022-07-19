# Projeto do Simulador MIPS

- Aluno: Marcos Frederico Raposo Hayman
- Disciplina: Arquitetura de Computadores
- Turma B1: 2022 / 1º

## Como usar

- Rode o programa main.
- O programa perguntará qual o arquivo que deseja simular (Deve ter a extensão .asm).
- Insira o caminho e o nome do arquivo a partir da pasta em que o programa está sendo rodado.
- Se não houver erros, será vista a mensagem `"Simulação bem sucedida!"`
- Ao ver essa mensagem, dentro da pasta [resultado](resultado) terão sido gerados 3 arquivos: [pipeline.csv](resultado/pipeline.csv), [registradores.csv](resultado/registradores.csv) e [memoria.csv](resultado/memoria.csv)
- Cada um desses arquivos gerados mostra o histórico de cada ciclo.
- Por exemplo, caso queire rodar o arquivo [multiplicacao.asm](multiplicacao/multiplicacao.asm):

```
pyhton main.py
Digite o nome do arquivo de entrada:
multiplicacao/multiplicacao
Simulação bem sucedida!
```
