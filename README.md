processaDir
===========

Script para ler e processar o conteúdo de um arquivo dump gerado por um comando dir full do sistema windows, tem por finalidade detectar e filtrar dados deste arquivo, como separar por extensões, verificar qual delas estão em branco ou com acentuação e tratar isso, nomes de diretórios em branco, etc...


Forma de usar:

$ python processaDir.py -a <nomeArquivo> -f <ftpserver>


Futuras implementações:

- Buscar o arquivo em um servidor FTP
- Aplicar um filtro no resultado por extenção. 