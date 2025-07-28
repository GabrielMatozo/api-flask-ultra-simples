# Derivando da imagem oficial do MySQL 5.7
FROM mysql:5.7

# Adicionando os scripts SQL para serem executados na inicialização do banco
COPY ./db/ /docker-entrypoint-initdb.d/
