# Redalyc crawler
Tem como finalidade fazer busca sistemática na base de dados Redalyc

O que motivou a criação desse robô:
* A plataforma Redalyc não tem as funções de operadores booleanos entre grupos;
* Não tem a funcionalidade de exportar os resultados de pesquisa;


# Autor
Luiz Eduardo Pizzinatto


# Execução
1. O primeiro passo é baixar e instalar o _Python 3.*_ em https://www.python.org/downloads/
1. Depois, crie uma pasta qualquer em seu computador e baixe e descompte os arquivos do robô. Disponíveis em: https://github.com/pizzinatto22/redalyc_crawler/archive/master.zip
1. Execute o arquivo `instalar_bibliotecas_python.bat`
1. Criar os arquivos `grupo1.txt`, `grupo2.txt`, `grupo3.txt`, etc. Cada arquivo para um grupo de descritores. E cada descritor em uma linha. Exemplos:
 * Arquivo1: `grupo1.txt`
  * Universidades
  * Gestão_universitária
  * Instituições_de_ensino_superior
 * Arquivo2: `grupo2.txt`
  * gestão_democrática
  * gestão_participativa
  * democracia
1. Execute o arquivo `executar.bat`
 1. Será criado um arquivo chamado `artigos.csv` com o resultado de todas as consultas, posteriormente, o robô fará uma análise para exclusão de resultados iguais (pela id do artigo), gerando um arquivo `artigos_não_duplicados.csv`.
1. O arquivo `artigos_não_duplicados.csv` deverá ser aberto pelo LibreOffice, selecionando o conjunto de caracteres "Unicode UTF-8".

# Informações
Observações da estrutura de busca:
- Para consultar uma expressão como `Gestão Universitária` deve se utilizar o underline entre palavras e não usar aspas, ex. `gestão_universitária`
- dentro de um mesmo grupo, a plataforma assume o operador booleano OR, entre grupos, assume o operador booleano AND. Então, no exemplo acima, seria equivalente a sintaxe de busca:
`("universidades" OR "gestão universitária" OR "instituições de ensino superior") AND ("gestão democrática" OR "gestão participativa" OR "democracia")`
Ou seja, qualquer elemento do grupo 1 com qualquer elemento do grupo 2
- Podes criar quantos grupos forem necessários, bastando criar arquivos `grupo3.txt`, `grupo4.txt`, etc.
- O número de consultas que o robô fará à base é a multiplicação dos números de descritores de cada grupo. Ou seja, se tiver três grupos com dois descritores cada, o total de consultas será 8, pois, 2x2x2=8
