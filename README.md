# Controle-de-ativos

## Trabalho de Cibersegurança

 - Criado um repositorio para ficar responsavel para atuar no banco de dados

 - riado os as classes para os dtos

 - Criado o service para ter a responsabilidade de atuar nos ativos

 - Criado Menu para usuario poder interagir pelo terminal

 - Adicionado manipulação de arquivo

 - Ajustado arquivo para usar dicionario

## Análise de risco

O cálculo usa NumPy para montar a matriz de incidência e o vetor CVSS, validar a invertibilidade e o condicionamento de `I - A`, e resolver o sistema `(I - A)x = b` com `numpy.linalg.solve`. As dependências incluem NumPy em `requirements.txt`; para atualizar uma instalação Docker, reconstrua a imagem com `docker compose up -d --build`.

O fator de transmissão é definido pelo tipo do ativo que recebe o risco: servidor `0,8`, software `0,5`, aplicação `0,5`, banco de dados `0,7` e equipamento `0,3`. Ao cadastrar uma dependência, a aplicação usa esse fator automaticamente; não é necessário informá-lo no formulário.

A severidade da vulnerabilidade é derivada da nota CVSS: baixa `[0, 3)`, média `[3, 6)`, alta `[6, 9)` e crítica `[9, 10]`. A classificação é exibida automaticamente no formulário e recalculada ao salvar; na inicialização, registros existentes também têm a severidade sincronizada com sua nota.
