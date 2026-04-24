Fase 2 - Analisador Sintático LL(1)

- Instituição:PUCPR
- Disciplina: Linguagens Formais e Compiladores
- Professor: Frank Coelho de Alcantra
- Aluno: Lucas Ferraz
- GitHub do aluno: FerrazLucas

Sobre o projeto
Este projeto foi feito para a Fase 2 da disciplina.

A ideia é ler um arquivo de entrada no formato da linguagem proposta, fazer a análise sintática usando uma abordagem LL(1), montar a árvore sintática e gerar o código Assembly.

O que o programa faz
O programa:
- lê o arquivo de entrada;
- faz a tokenização de cada linha;
- verifica se o programa começa com `(START)` e termina com `(END)`;
- faz a análise sintática;
- monta a árvore sintática;
- salva a árvore em JSON;
- salva um resumo da gramática, FIRST, FOLLOW e tabela LL(1);
- gera o arquivo Assembly.

Arquivos principais
- main.py: código principal do projeto
- tokens_saida.txt: saída com os tokens reconhecidos
- arvore_saida.json: árvore sintática gerada
- analise_sintatica.txt: gramática, FIRST, FOLLOW e tabela LL(1)
- saida.s: código Assembly gerado

Como executar
No terminal, rode:
python main.py arquivo.txt

Exemplo:
python main.py teste1.txt

## Estrutura geral do programa
Todo arquivo de entrada deve seguir esta ideia:

(START)
...comandos...
(END)

A primeira linha precisa ser (START) e a última linha precisa ser (END).

Sintaxe aceita

1. Expressões aritméticas em notação polonesa reversa
Exemplos:


(2 3 +)
(10 2 -)
(4 5 *)
(9 2 |)
(9 2 /)
(9 2 %)
(2 3 ^)


2. Uso de memória
Guardar valor em memória:


((2 3 +) X)


Ler valor da memória:


(X)


3. Referência a resultado anterior com RES
Exemplo:
(1 RES)
Isso pega o resultado de uma linha executável anterior.

4. Estruturas de decisão e repetição

IF
Executa o comando se a condição for diferente de zero.

(<condicao> <comando> IF)

Exemplo:
((1) (2 3 +) IF)

IFELSE
Executa o primeiro comando se a condição for diferente de zero. Se for zero, executa o segundo.

(<condicao> <comando> <comando> IFELSE)

Exemplo:
((0) (2 3 +) (4 5 *) IFELSE)

WHILE
Repete enquanto a condição for diferente de zero.

(<condicao> <comando> WHILE)

Exemplo:
((0) (9 Y) WHILE)

#Regras usadas no projeto
- valor diferente de 0 significa verdadeiro;
- valor igual a 0 significa falso;
- | foi usado para divisão real;
- / foi usado para divisão inteira;
- % representa resto da divisão;
- ^ representa potência.

Exemplo de entrada

(START)
(2 3 +)
((1 RES) X)
((X) 2 |)
((1) (7 8 +) IF)
((0) (1 2 +) (3 4 +) IFELSE)
((0) (9 Y) WHILE)
(END)

Exemplo de saída
Depois da execução, o programa gera:
- tokens_saida.txt
- arvore_saida.json
- analise_sintatica.txt
- saida.s

Testes
Foram criados arquivos de teste válidos e inválidos para verificar:
- operações aritméticas;
- uso de memória;
- uso de RES;
- estruturas IF, IFELSE e WHILE;
- erros léxicos;
- erros sintáticos.
