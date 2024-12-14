# Simplex Revisado

Exercício programa desenvolvido por Matheus Silveira Feitosa, email: matheus.feitosa@usp.br do Instituto de Matemática e Estatística da Universidade de São Paulo (IME-USP).


## Índice 

- [Título e Autores](#Simplex Revisado)
- [Índice](#índice)
- [Descrição do Projeto](#descrição-do-projeto)
- [Como Executar o Programa](#como-executar-o-programa)
- [Dependências](#dependências)

## Descrição do Projeto

### Programa Principal
O projeto foi feito visando fornecer ao estudante de Otimização Linear, uma introdução ao método Simplex Revisado visto na segunda parte do curso de MAC0315 do IME-USP.

Com tal objetivo em mente, foi construído um programa que seja capaz de receber como entrada, um problema qualquer de otimização linear, e então, gerar um documento em latex contendo o passo a passo da solução.

## Como Executar o Programa
Para utilizar apenas o solver, basta importar de Solver a classe RevisedSimplex e passar a equação no formato detalhado dentro do método solve.

Caso queira gerar o documento Latex, basta marcar showSteps = true, que então, o documento Latex será gerado dentro da pasta output em data/

## Dependências
numpy

********