import csv

#constantes
ARQUIVO = "artigos.csv"
ARQUIVO_PROCESSADO = "artigos_processados.csv"

csvfile = open('artigos.csv')
csvreader = csv.reader(csvfile)

data = {}

print("Removendo os artigos duplicados do arquivo '{}'".format(ARQUIVO))

artigos_originais = 0;
artigos_sem_duplicados = 0
for row in csvreader:
	artigos_originais += 1
	if row[0] not in data:
		artigos_sem_duplicados += 1
		data[row[0]] = row


f = open(ARQUIVO_PROCESSADO, "w")
for d in data:
	row = '";"'.join(d)
	f.write('"{}"\n'.format(row))

f.close()

print("Foram encontrados {} artigos. Após o processamento sobraram {}".format(artigos_originais, artigos_sem_duplicados))
print("\n\nArquivo '{}' gerado com sucesso.".format(ARQUIVO_PROCESSADO))
