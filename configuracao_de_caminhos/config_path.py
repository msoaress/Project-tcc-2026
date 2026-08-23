# config.py
from pathlib import Path

# 1. O Python descobre automaticamente onde a pasta "projeto assistente Ia - versão 2.0" está no computador atual
RAIZ_PROJETO = Path(__file__).resolve().parent.parent

# 2. Mapeamento genérico de todas as pastas que você usa
APP_BANCO = RAIZ_PROJETO / "pasta_banco_para_producao"
APP = RAIZ_PROJETO / "APP"

# Subpastas específicas
<<<<<<< HEAD
PASTA_IMAGENS = APP / "front_end" / "imagens"
PASTA_PROMPT = APP / "prompt"
PASTA_BANCO_PROD = APP_BANCO  / "banco_em_produção"
=======
PASTA_IMAGENS = APP  / "front_end" / "imagens"
PASTA_PROMPT = APP / "prompt"
PASTA_BANCO_PROD = APP_BANCO / "banco_em_produção"
>>>>>>> 5eab403 (adaptação doc aminha da pasta)
# 3. Garante que as pastas de banco e arquivos existam no SO do usuário
PASTA_BANCO_PROD = Path("pasta_banco_para_producao") / "banco_em_produção"

PASTA_BANCO_PROD.mkdir(parents=True, exist_ok=True)
