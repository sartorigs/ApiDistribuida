# Busca distribuída entre servidores

## Objetivo

O objetivo deste projeto é implementar um sistema de busca distribuída entre servidores. O sistema deve ser capaz de buscar documentos em diferentes apis e bancos separados utilizando do DFS para as buscas.

## Observações

O algoritmo de busca utilizado é o DFS (Depth First Search), e o docker-compose.yml está configurado para rodar 5 servidores, cada um com um banco de dados diferente.