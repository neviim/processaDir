#!/usr/bin/python
# *-* coding: utf-8 *-*

# por: Neviim
# data: Inicio: 21/06/2012  Fim:
# Para executar: python processaDir.py

import operator
import getopt
import sys
import re

SCRIPT_NOME = "processaDir"
SCRIPT_AUTOR = "Neviim JADS"
SCRIPT_VERSAO = "0.5"
SCRIPT_LICENCA = "GPL3"
SCRIPT_DESCRICAO = "Le e estrutura um arquivo com arvore de diretorios"

def nvExtensao(arquivo):
	"""verifica se o arquivo tem uma extensao e retorna ela,
	   uso: > nvExtensao("arquivo.txt")
	   Retorna se encontrar: '.txt'
	   Retorna se nao achar: -1           
	"""
	lista = arquivo.split('.')
	if len(lista) > 1: 
	   return lista[len(lista)-1].lower()
	else:
		return -1

	pass

# Chamada principal
def main(argv):
	
	fileAcesso = ""

	try:
		opts, args = getopt.getopt(argv,"ha:f:",["arquivo=","ftpserver="])
	except getopt.GetoptError:
		print 'processaDir.py -a <nomeArquivo> -f <ftpserver>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'processaDir.py -a <nomeArquivo> -f <ftpserver>'
			sys.exit()
			
		elif opt in ("-a", "--arquivo"):
			fileAcesso = open(arg,"r")
			
		elif opt in ("-f", "--ftpserver"):
			fileServer = arg

	if fileAcesso == "":
	   return()

	"""declara as variaveis a serem totalisadas durante a operacao"""
	espacoEmDiscoTotal = 0  # Total de espaco em disco ocupado
	espacoEmDiscoProce = 0  # Total de espaco em disco Processado
	contador_total = 0      # Total de linhas processadas
	contador_valido = 0     # Total de linhas validadas
	contador_semext = 0     # Total de erros sem extensao 
	contador_dir = 0        # Total de diretorios
	contador_sub = 0        # Total de diretorios validos
	extensao_soma = 0       # Total de soma das extensoes
	extensao_arquivos = 0   # Total de arquivos com estensao
	
	extensaoDict = {} 		# Contador de quantidade de arquivo por estensoes e consumo em disco.
	
	# Inicio do processamento...
	for line in fileAcesso:
		strLines = line
		strTemp = re.sub(' +',' ',strLines)		# Retira os espaços duplos.
		strLimp = re.split(" ",strTemp) 		# separa os conteudos.
		contador_total+=1
		
		# Debug...
		#print unicode(strTemp, 'utf-8-sig', 'ignore')
		
		# Filtro para arquivos e diretorios
		if str(strLimp[0]).count("/") == 2:
			
			# Se o conteudo em strLimp[2] não for "<DIR>" ele podera ser o valor numerio espaço ocupado em disco, por ex.
			if str(strLimp[2]) <> "<DIR>":
				nome = str(strLimp[3]).rstrip("\n")
				nome = nome.rstrip("\r")
				
				#extensao = nome[len(nome)-4:len(nome)].lower()
				extensao = nvExtensao(nome)
				espacoEmDisco = int(re.sub("\D", "",strLimp[2]))  # Deixa só os numeros na estring
				espacoEmDiscoTotal += int(re.sub("\D", "",strLimp[2]))  # Deixa só os numeros na estring
				
				#if contador_total >= 10:
				#   return
				
				# Tem que ser um arquivo com extenção e tamanho maior que 0.
				if extensao <> -1: 
					espacoEmDiscoProce += int(re.sub("\D", "",strLimp[2]))  # Deixa só os numeros na estring
					
					# Arquiva as extensoes que forem encontradas.
					if str(extensao) not in extensaoDict:
						extensaoDict[extensao] = {'quantidade': 0, 'bytes': 0}
						
					extensaoDict[extensao] = {'quantidade': extensaoDict[extensao]['quantidade']+1, 'bytes': extensaoDict[extensao]['bytes']+espacoEmDisco}  
					contador_valido+=1
					 
					# Debug...
					#print str(strLimp[0]) +' * '+ str(strLimp[1]) +' * '+ str(strLimp[2]) +' * '+ str(nome) +' * '+ str(extensao)
					
				else:
					# Nomes sem estensao, grava todos em um unico campo.
					if 'semExt' not in extensaoDict:
						extensaoDict['semExt'] = {'quantidade': 0, 'bytes': 0}
					
					extensaoDict['semExt'] = {'quantidade': extensaoDict['semExt']['quantidade']+1, 'bytes': extensaoDict['semExt']['bytes']+espacoEmDisco} 
					contador_semext+=1
					
					# Debug...
					#print str(strLimp[0]) +' * '+ str(strLimp[1]) +' * '+ str(strLimp[2]) +' * '+ unicode(str(nome),'utf-8-sig','ignore') +' * '+ unicode(str(extensao),'utf-8-sig','ignore')					
				
			else:
			    #Se for um "<DIR>"
			    contador_dir+=1
			    
			    if str(strLimp[2] == "<DIR>"):
					strDiretorio = unicode(str(strLimp[3]).rstrip("\n"), 'utf-8-sig', 'ignore')
					
					if strDiretorio[0:1] <> ".":
						contador_sub+=1 # contador do subdiretorio processado.
						
			       		# Debug...
						#print strDiretorio
						#print str(strLimp[2]) # Esta variavel contel o "<DIR>" str(strLimp[2])
						#print unicode(strTemp, 'utf-8-sig', 'ignore')
							
	
    # Imprime os resultados obtidos no processamento do arquivo texto.
	print "Quantidade de espaco que ocupamos atualmente:"
	print
	print "Total de linhas no arquivo:  " + str(contador_total)
	print "Total de linhas  apuradas:   " + str(contador_valido)
	print "Total de diretorios:         " + str(contador_dir)
	print "Total de diretorios '.''..': " + str(contador_sub)
	print "Total de diret sem extensao: " + str(contador_semext)
	print "Total de disco processado:   " + str(espacoEmDiscoProce)
	print "Total de disco usado:        " + str(espacoEmDiscoTotal)
	print 
	print "Total ocupado em Gigabyte:   " + str(espacoEmDiscoTotal / 1073741824)
	print "Total ocupado em Megabyte:   " + str(espacoEmDiscoTotal / 1048576)
	print "Total ocupado em Kilobyte:   " + str(espacoEmDiscoTotal / 1024)
	print 

	print "Estensoes: "
	print
	print 'Extensao'.ljust(20,'-') +' '+ 'Quantida'.rjust(8,'-') +' '+ 'bytes'.rjust(20,'-')
	print '-'.rjust(50,'-')
	#
	# Loop para totalizar e imprimir as extensoes.
	
	for ext in sorted(extensaoDict.keys(), key=str):
		print str(ext).ljust(20,' ') +' '+ str(extensaoDict[ext]['quantidade']).rjust(8,' ') +' '+ str(extensaoDict[ext]['bytes']).rjust(20,' ')
		extensao_soma+=extensaoDict[ext]['bytes']
		extensao_arquivos+=extensaoDict[ext]['quantidade']
	
    # Imprime resumo da lista impresa.
	print '-'.rjust(50,'-')
	print 'Total:   '.ljust(21,' ') +str(extensao_arquivos).rjust(8,' ') +' '+ str(extensao_soma).rjust(20,' ')
	print
	print 'Gigabyte '.ljust(39,'.') +str(extensao_soma / 1073741824).rjust(11,' ')
	print 'Megabyte '.ljust(39,'.') +str(extensao_soma / 1048576).rjust(11,' ')
	print 'Kilobyte '.ljust(39,'.') +str(extensao_soma / 1024).rjust(11,' ')
		
	# Fecha arquivo texto aberto.
	file.close(fileAcesso)
	
	pass

if __name__ == '__main__':
	main(sys.argv[1:])