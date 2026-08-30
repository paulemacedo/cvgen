# CV Generator

Gerador de currículos em HTML/PDF com templates profissionais, suporte a múltiplos idiomas e CLI organizada para produção.

## Visão geral

O projeto lê dados em JSON, renderiza templates HTML com Jinja2 e exporta o resultado em PDF usando Playwright/Chromium. A estrutura foi dividida em módulos para separar:

- conteúdo do perfil
- localização e tradução
- preparação dos dados
- templates e assets
- geração e exportação
- interface de linha de comando

## Requisitos

- Python 3.10+
- pip
- Chromium/Playwright para geração de PDF

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/paulemacedo/CV-Generator.git
cd CV-Generator
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

3. Instale as dependências:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

4. Instale o navegador para PDF:

```bash
python -m playwright install chromium
```

## CLI

Após a instalação, o comando global fica disponível:

```bash
cvgen --help
```

### Comandos disponíveis

```bash
cvgen generate --profile all --template blackluxury --language pt --format pdf
cvgen generate --profile paule --template blackluxury --language pt --format html
cvgen templates
cvgen profiles
cvgen validate
```

### Sintaxe curta suportada

Também funciona a versão direta sem subcomando e com aliases curtos:

```bash
cvgen --template blackluxury
cvgen -t blackluxury
cvgen --language pt
cvgen -l pt
cvgen --profile all --template ivory
cvgen -p all -t ivory
```

### Parâmetros principais

- `--profile`, `-p`: nome do perfil ou `all`
- `--template`, `-t`: `ivory`, `paule`, `blackluxury`, ou `all`
- `--language`, `-l`: `pt`, `en`, ou `all`
- `--format`, `-f`: `pdf` ou `html`

## Estrutura do projeto

```text
CV-Generator/
├── src/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   ├── data.py
│   ├── export.py
│   ├── generator.py
│   ├── localization.py
│   ├── paths.py
│   └── prepare.py
├── data/
│   ├── Examples/
│   ├── support.json
│   ├── vaga-c-verde.json
│   └── ...
├── templates/
│   ├── BlackLuxury.html
│   ├── BlackLuxury.css
│   ├── Ivory.html
│   ├── Ivory.css
│   ├── Paule.html
│   ├── Paule.css
│   ├── common.css
│   └── ...
├── output/
├── tests/
│   ├── test_cli.py
│   └── test_summary_template.py
├── generate.py
├── pyproject.toml
├── requirements.txt
├── README.md
└── ...
```

## Uso em linha de comando

### Gerar todos os perfis

```bash
cvgen generate --profile all --template all --language all --format pdf
```

### Gerar um perfil específico

```bash
cvgen generate --profile support --template blackluxury --language pt --format pdf
```

### Gerar apenas HTML para ajustes visuais

```bash
cvgen generate --profile all --template blackluxury --language pt --format html
```

Os arquivos gerados ficam em `output/` e em `output/temp/` conforme o fluxo do projeto.

## Dados e perfis

Os perfis ficam em `data/` e são arquivos JSON. Cada arquivo define informações como:

- nome
- headline
- resumo
- experiência
- educação
- projetos
- skills
- contato
- publicações
- certificações

O gerador detecta automaticamente os idiomas disponíveis no perfil e renderiza somente os arquivos que fazem sentido para aquele JSON.

## Templates

Os templates disponíveis atualmente incluem:

- `ivory`
- `paule`
- `blackluxury`

Você pode usá-los com as versões longas ou curtas da CLI:

```bash
cvgen --template blackluxury
cvgen -t blackluxury
cvgen generate --template blackluxury
cvgen generate -t blackluxury
```

A especialização principal do projeto foi no tema `blackluxury`, com layout single-column, leitura profissional e exportação PDF mais estável.

## Validação

Para validar os perfis e a estrutura do CLI:

```bash
cvgen validate
python -m unittest discover -s tests -v
```

## Licença

Este projeto está em desenvolvimento e pode ser adaptado para uso pessoal ou colaborativo. Consulte o arquivo de licença correspondente no repositório, se houver.

## Observações

- A geração de PDF depende do Chromium do Playwright.
- O comando `cvgen` funciona após instalação em modo editable, via `pip install -e .`.
- A compatibilidade com o script legado `generate.py` foi mantida para facilitar uso e migração gradual.
