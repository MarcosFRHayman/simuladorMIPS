## Coisas a se fazer:

- percorrer o arquivo
- fazer um map da label para a linha da label (assim como no montador)
- fazer um map de cada instrução para um objeto (assim como no montador)
- a cada ciclo chamar a função correspondente à etapa do pipeline em que ela se encontra
- a cada ciclo escrever os valores dos bancos de registradores, memória principal e pipeline
- gerar os arquivos

## Estratégias possíveis:

- Objeto de Pipeline pode ter um campo para o seu CSVBuffer
- Pipeline deve ter um método "avança ciclo do pipeline" que recebe a nova instrução para se por em em ID, avançar todas as instruções para o próximo ciclo e remover da lista a instrução em WB

## Entrega do trabalho (zipado):

- README explicando como usar o programa
- código fonte
- arquivos usados para teste
- Slide com apresentação do projeto
