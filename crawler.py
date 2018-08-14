import html
import re
import requests #precisa instar com pip install requests OU python3 -m pip install requests
import sys

from lxml import html as et
from os import listdir, path, remove

#constantes
ARQUIVO = "artigos.csv"

#gerando as combinações entre todos os grupos para formar cada uma das queries
def combine(list1, list2):
	combinated = []
	for i in list1:
		for j in list2:
			combinated.append(i + " AND " + j)
	return combinated

def baixar_conteudo(url, pagina):
	print("      (baixando a pagina {})".format(pagina))
	req = requests.get(url)

	text = req.text.replace("&amp;", "&")
	text = html.unescape(text)

	#parser = et.HTMLParser()
	#return et.XML(text, parser = parser)
	return et.fromstring(text)

def clean(tag):
	return tag.text_content().replace("\n", " ").replace("\t", "").replace('"',"").replace(",","").strip()

def extrair_dados(xml, query):
	#abre e fecha o arquivo em cada análise, para evitar de perder tudo, caso haja algum erro durante o percurso
	f = open(ARQUIVO, "a+", encoding="utf-8")

	#pega todos os artigos da pagina
	linhas = xml.xpath("//div[@id='lista']//table[contains(@class, 'dr-table')]//tr[contains(@class, 'dr-table-row')]")

	#processa cada um dos artigos
	for l in linhas:

		#cada artigo está dentro de uma tabela, contendo 5 linhas
		dados_artigo = l.xpath(".//table/tbody/tr")

		titulo = clean(dados_artigo[0])
		autores = clean(dados_artigo[1])
		revista = clean(dados_artigo[2])

		link = dados_artigo[0][0][0].get("href")

		f.write('"http://www.redalyc.org/{}";"{}";"{}";"{}";"{}"\n'.format(link, titulo, autores, revista, query))


			#Título do Artigo; Autores; Revista; Link para o texto completo., depois uma limpeza na tabela para excluir os resultad

	f.close()


#groups é uma lista que vai conter as palavras de cada grupo
groups = [];
for fileName in listdir():
	if fileName.lower().startswith("grupo"):
		file = open(fileName, "r");
		groups.append(file.read().splitlines())

if not len(groups):
	print("Não foram econtrados arquivos com o nome 'grupo*.*'");
	sys.exit(1);

#fazendo a permuta entre os grupos
queries = groups[0];
if len(groups) > 1:
	for i in range(1, len(groups)):
		queries = combine(queries, groups[i])


if path.isfile(ARQUIVO) and input("Já existe um arquivo chamado '{}'. Deseja excluí-lo e iniciar do zero (S/N)?\n(Caso queira que o robô continue incrementando o arquivo, responda N): ".format(ARQUIVO)).lower() == "s":
	remove(ARQUIVO)

URL = r"http://www.redalyc.org/busquedaArticuloFiltros.oa?q={}&idp={}"
i = 0
total_queries = len(queries)

for q in queries:
	i += 1
	pagina_corrente = 1

	#inicializando pesquisa
	url = URL.format(q, pagina_corrente)
	print("Pesquisando: '{}' ({})".format(q, url))
	print("   Este é o conjunto de termos {}/{}".format(i, total_queries))

	#baixando a primeira página desse conjunto de termos
	xml = baixar_conteudo(url, pagina_corrente)


	#pegando dados para saber quantos artigos e páginas serão analisadas
	texto_total_artigos = xml.xpath("//span[@class='txt-total-art']/text()")

	qt_artigos = 0
	if (texto_total_artigos and len(texto_total_artigos)):
		parse_qt_paginas = re.findall(r"[0-9]* - [0-9]* de ([0-9]*) docume", texto_total_artigos[0], re.I)
		if (len(parse_qt_paginas)):
			qt_artigos = int(parse_qt_paginas[0])

	if (not qt_artigos):
		print("   *** Nao foi possível determinar a quantidade de artigos")
	else:
		total_paginas = int(qt_artigos/10)
		if (total_paginas != qt_artigos/10.0):
			total_paginas += 1

		print("   Foram encontrados {} artigos, totalizando {} paginas".format(qt_artigos, total_paginas))

	print("\n")
	print("    **** Iniciando a análise **** ")


	#analisando as páginas da pesquisa atual
	while pagina_corrente <= total_paginas:
		print("       Analisando a página {}/{}".format(pagina_corrente, total_paginas), end="")
		extrair_dados(xml, q)
		print(" > Análise concluída!")

		#pegando dados da próxima pagina
		pagina_corrente += 1
		url = URL.format(q, pagina_corrente)
		if pagina_corrente <= total_paginas:
			xml = baixar_conteudo(url, pagina_corrente)
