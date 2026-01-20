# yt-audio-downloader

CLI em Python para download de áudio a partir de vídeos do YouTube, utilizando a biblioteca **yt-dlp** e seguindo boas práticas de desenvolvimento de software.

O projeto foi desenvolvido com foco em:
- organização modular,
- tipagem estática,
- logging estruturado,
- separação de responsabilidades,
- facilidade de extensão futura.

---

## Funcionalidades

- Download de áudio a partir de uma ou mais URLs do YouTube
- Extração automática do melhor áudio disponível
- Conversão para diferentes formatos:
  - `mp3`
  - `m4a`
  - `opus`
- Controle de qualidade do áudio (quando aplicável)
- Suporte opcional a playlists
- Interface de linha de comando (CLI)
- Estrutura compatível com projetos profissionais em Python

---

## Estrutura do Projeto

```text
yt-audio-downloader/
├─ src/
│  └─ yt_audio_downloader/
│     ├─ cli.py              # Interface CLI
│     ├─ downloader.py       # Lógica de download
│     ├─ config.py           # Configurações do projeto
│     └─ logging_utils.py    # Logging centralizado
├─ tests/                    # Testes unitários
├─ pyproject.toml            # Dependências e ferramentas
└─ README.md
```

To run: 
```bash
pip install -r requirements.txt
```
To Dev and Run:
```bash
pip install -r requirements.txt -r requirements-dev.txt
```

Verificar FFmpeg (obrigatório para extrair/convert. áudio)
```bash
ffmpeg -version
```
Rodar lint/format e tipagem (qualidade de código)
```bash
ruff format .
ruff check .
mypy src
```
Rodar testes unitários
```bash
pytest -q
```

Windows PowerShell
```bash
$env:PYTHONPATH="src"
python -m yt_audio_downloader.cli "https://www.youtube.com/watch?v=XXXX"
```
