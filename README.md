# Controle de Ativos

Aplicação web em Python com Flask para inventariar ativos de TI, cadastrar vulnerabilidades, relacioná-las aos ativos e consultar o risco próprio e efetivo. Os dados ficam em banco relacional MariaDB quando executada com Docker Compose.

## Funcionalidades

- Cadastro, listagem, edição e remoção de ativos e vulnerabilidades.
- Associação e remoção de vínculos entre ativos e vulnerabilidades.
- Login obrigatório para acessar as telas do sistema. Não há cadastro público de usuários.
- Nota CVSS de 0 a 10 por vulnerabilidade. A severidade é calculada automaticamente:
  - **Baixa:** de 0 até menos de 3.
  - **Média:** de 3 até menos de 6.
  - **Alta:** de 6 até menos de 9.
  - **Crítica:** de 9 até 10.
- Cadastro de dependências entre ativos. O fator de transmissão é definido pelo tipo do ativo que recebe o risco: servidor `0,8`, software licenciado `0,5`, aplicação `0,5`, banco de dados `0,7` e equipamento `0,3`.
- Consulta do risco próprio e do risco efetivo de cada ativo.

## Modelo de risco

Com `n` ativos e `m` vulnerabilidades, a aplicação forma a matriz de incidência `M` (`n × m`) e o vetor `v` com as notas CVSS. O risco próprio é `b = Mv`.

A matriz `A` registra o risco transmitido entre ativos. Se o ativo **A depende do ativo B**, a linha de A e a coluna de B recebem o fator de transmissão da classe de A. O risco efetivo é obtido resolvendo `(I - A)x = b` com `numpy.linalg.solve`.

Antes de resolver, o sistema verifica a invertibilidade e o número de condição de `I - A`. A soma das frações de dependência que chegam a cada ativo deve ser menor que `1`; caso contrário, ou se o sistema estiver mal condicionado, o cálculo é recusado. O fator de transmissão é aplicado automaticamente pelo servidor e não é informado manualmente no formulário.

## Requisitos

- Docker Engine e Docker Compose v2 para executar a configuração recomendada.
- Ou Python 3.12 ou superior para executar sem Docker.

## Executar com Docker Compose

1. Clone o repositório e entre na pasta:

   ```bash
   git clone URL_DO_REPOSITORIO controle-de-ativos
   cd controle-de-ativos
   ```

2. Crie o arquivo de configuração local e edite os valores:

   ```bash
   cp .env.example .env
   openssl rand -hex 24
   openssl rand -hex 24
   openssl rand -hex 32
   nano .env
   chmod 600 .env
   ```

   Use os valores aleatórios gerados para `DB_PASSWORD`, `DB_ROOT_PASSWORD` e `SECRET_KEY`. O arquivo `.env` contém segredos e não deve ser enviado ao repositório.

3. Construa e inicie a aplicação e o MariaDB:

   ```bash
   docker compose up -d --build
   docker compose ps
   ```

4. Crie o usuário de acesso:

   ```bash
   docker compose exec app flask --app app create-admin
   ```

   O comando solicita o nome do usuário e uma senha com pelo menos 12 caracteres. A senha é armazenada como hash.

5. Acesse `http://IP_DO_SERVIDOR:666` e entre com o usuário criado. Se o acesso for remoto, libere a porta TCP `666` no firewall do servidor e nas regras de rede do provedor.

O MariaDB não publica a porta `3306` no servidor: somente a aplicação o acessa pela rede interna do Compose. Os dados do banco ficam no volume Docker `mariadb_data`, que persiste mesmo quando os containers são recriados.

### Configuração do Docker

As variáveis são definidas no `.env`:

| Variável | Uso |
|---|---|
| `DB_NAME` | Nome do banco MariaDB. |
| `DB_USER` | Usuário da aplicação no banco. |
| `DB_PASSWORD` | Senha do usuário da aplicação no banco. |
| `DB_ROOT_PASSWORD` | Senha administrativa do MariaDB. |
| `SECRET_KEY` | Chave aleatória usada para assinar a sessão de login. |
| `COOKIE_SECURE` | Use `true` quando houver HTTPS configurado; caso contrário, `false`. |

Para atualizar a aplicação após enviar mudanças ao repositório:

```bash
git pull
docker compose up -d --build
```

Para consultar logs:

```bash
docker compose logs --tail=100 app
docker compose logs --tail=100 mariadb
```

**Atenção:** `docker compose down -v` remove também o volume do banco e apaga os dados. Não use esse comando para uma atualização normal. Faça backup antes de operações destrutivas ou mudanças no banco.

## Executar localmente sem Docker

Crie e ative um ambiente virtual, instale as dependências e configure uma chave de sessão:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="$(openssl rand -hex 32)"
```

Sem `DATABASE_URL` ou `DB_HOST`, a aplicação usa SQLite local. Crie o usuário e inicie o servidor:

```bash
flask --app app create-admin
flask --app app run --host 0.0.0.0 --port 666
```

Abra `http://127.0.0.1:666`. Para usar MariaDB local ou externo, configure `DATABASE_URL` **ou** `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` e `DB_PASSWORD` no ambiente antes de iniciar.

## Persistência e compatibilidade

Na inicialização, a aplicação cria as tabelas necessárias. Se uma base anterior ainda não tiver `cvss_score`, essa coluna é adicionada e recebe `0` para os registros antigos; em seguida, a severidade de cada vulnerabilidade é sincronizada com sua nota CVSS. Faça backup antes de apontar a aplicação para um banco com dados importantes.

## Testes

Com as dependências instaladas, execute:

```bash
python -m unittest discover -s tests -v
```
