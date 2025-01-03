# Método Simplex Revisado

Exercício-programa desenvolvido por **Matheus Silveira Feitosa**  
Instituto de Matemática e Estatística da Universidade de São Paulo (IME-USP)

## Índice

- [Título e Autores](#método-simplex-revisado)
- [Índice](#índice)
- [Descrição do Projeto](#descrição-do-projeto)
- [Como Executar o Programa](#como-executar-o-programa)
- [Dependências](#dependências)

## Descrição do Projeto

### Programa Principal
Este exercício programa foi proposto com o objetivo de fornecer uma ferramenta prática e didática para futuros estudantes de **Otimização Linear** durante os estudos do método do **Simplex Revisado**, que é abordado na segunda parte do curso **MAC0315 - Programação Linear** no IME-USP.

Com tal objetivo em mente, a implementação foi feita objetivando servir as seguintes funcionalidades:
- Resolução simples do método simplex usando do conteúdo visto em aula.
- Fornecimento de uma solução detalhada **passo a passo** do problema.

E como funcionalidades bônus foi proposto também os seguintes aspectos:

- Geração automática de um arquivo em **LaTeX** contendo cada etapa da execução.
- Suporte para leitura e escrita a partir de arquivos de entrada/saída permitindo a elucidação e input 
de problemas da mesma forma como são enunciados em classe.

## Como Executar o Programa
Para o uso simples, basta se certificar de possuir as [Dependências](#dependências) devidamente instaladas
e então dentro da pasta src, rodar o script Main.py, que a própria interface te guiará em seu uso.

Um dos requerimentos do programa é a existência de arquivos com problemas a serem resolvidos na pasta data/input
sendo assim, na primeira execução do programa, você encontrará um exemplo de como este arquivo pode ser feito.

Para mais detalhes, tem mais alguns exemplos, em conftest.py

Caso você esteja interessado apenas no Solver, você poderá utilizá-lo observando o exemplo na seção seguinte [Exemplo de uso manual](exemplo-de-uso-manual)

## Exemplo de Uso Manual

No caso de você não desejar utilizar arquivos, o programa também permite resolver problemas diretamente. Veja abaixo um exemplo onde um problema linear é resolvido com entradas diretas utilizando a classe `RevisedSimplexWithoutFile`.

### Problema de Exemplo:

Suponha o seguinte problema de **Maximização**:

Maximizar:  
`3x1 + 5x2`  

```plaintext
Sujeito a:  
            x1 + 2x2  ≤ 6  
            4x1 + 3x2 ≤ 12  
                   x2 ≥ 1  
            x1, x2 ≥ 0
```

### Código Python:

```python
import numpy as np
from Solver import RevisedSimplexWithoutFile

objective_function = np.array([3, 5])  # Vetor da função objetivo (c)
constraint_matrix = np.array([
    [1, 2],   # Primeira linha de restrições
    [4, 3],   # Segunda linha de restrições
    [0, 1]    # Terceira linha de restrições
])  # Matriz de restrições (A)

restrictions = np.array([6, 12, 1])  # Vetor do lado direito das restrições (b)
restriction_symbols = ["<=", "<=", ">="]  # Símbolos das restrições (opcional)
is_maximization = True  # Tipo do problema (se ele deve ser tratado como maximização ou minimzação)

# Instanciando o Solver e resolvendo o problema:
solver = RevisedSimplexWithoutFile(
    objective_function,
    constraint_matrix,
    is_maximization,
    restrictions,
    restriction_symbols
)

solver.solve(show_steps=False)  # Define se deve exibir os passos ou não
                                # Para o caso sem arquivo, você deverá instanciar 
                                # o LatexWriter por conta própria e indicar onde ele deverá escrever.
```

### Saída Esperada:

```plaintext
Solução ótima encontrada!
Variáveis básicas:  ['x2', 'x1', 's_3']
Valores:  {'x1': 1.2, 'x2': 2.4, 's_1': 0.0, 's_2': 0.0, 's_3': 1.4}
Máximo = 15.6000
Solução ótima encontrada:
x1 = 1.2
x2 = 2.4
s_1 = 0.0
s_2 = 0.0
s_3 = 1.4
```



## Dependências
Este projeto foi desenvolvido em Python 3 e utiliza as seguintes bibliotecas:

- **numpy**  

Para instalar as dependências, certifique-se de que o **Python 3.9+** está instalado, e utilize o comando:

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install numpy
```
---

E isso é todo o nescessário para rodar este EP em sua máquina.

********
