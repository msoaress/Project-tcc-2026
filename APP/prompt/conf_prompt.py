import sys
import os
from pathlib import Path

# Garante que o Python consiga encontrar arquivos na raiz do projeto
RAIZ = Path(__file__).resolve().parent.parent.parent
if str(RAIZ) not in sys.path:
    sys.path.append(str(RAIZ))

# Agora você importa direto do arquivo 'config.py'
from configuracao_de_caminhos.config_path import PASTA_PROMPT
# Adiciona a pasta raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class configuracao:

    def __init__(self):
        self.texto = ""       

    def extracao_prompt(self):
        
        arquivo = open(str(PASTA_PROMPT / "prompt.txt"),"r",encoding="utf-8")
        self.texto =  arquivo.read()
        arquivo.close()
        return self.texto