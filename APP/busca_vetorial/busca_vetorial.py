from anyio import sleep
import chromadb
import subprocess
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import os
import sys
from pathlib import Path

# Garante que o Python consiga encontrar arquivos na raiz do projeto
RAIZ = Path(__file__).resolve().parent.parent.parent
if str(RAIZ) not in sys.path:
    sys.path.append(str(RAIZ))

# Agora você importa direto do arquivo 'config.py'
from configuracao_de_caminhos.config_path import PASTA_BANCO_PROD
# Adiciona a pasta raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

#implementa essa solução amanha import os


class BuscaVetorial:


    def __init__(self, texto):
         
        self.texto = texto
        
        self.embedding_function = SentenceTransformerEmbeddingFunction(
            model_name="ibm-granite/granite-embedding-311m-multilingual-r2",
            device="cpu",

        )
        
        self.lista_dados_recuperados = []
        self.lista_completa_dados_recuperados = []
        self.texto_formatado = ""
        self.quantidade_de_documentos = 0
        self.endereco_bank =  PASTA_BANCO_PROD

    


    def recuperar_informacao(self):
        print("estou aqui")

        path = self.endereco_bank
        print(path)
            # Verifica se o banco existe e é válido
        db_file = os.path.join(path, "chroma.sqlite3")
        print(db_file) 
        quantidade_arq = len(os.listdir(path))
        print(quantidade_arq) 
        if  (os.path.exists(db_file)) and (quantidade_arq >= 2):       


            print(db_file)   
            
            
            client = chromadb.PersistentClient(self.endereco_bank)


            colecoes = client.list_collections()
            nome_colecao =  [colecao.name for colecao in colecoes]
            self.quantidade_de_documentos = len(nome_colecao)

            #print(f"coleções disponíveis: {nome_colecao}")

        else:

            colecoes = []


        if colecoes != [] :
           


            for nome in nome_colecao:
                
                collection = client.get_collection(name = nome,
                                                            embedding_function = self.embedding_function,
                                                                                                        
                                                            )
                
                results = collection.query(query_texts=[self.texto],n_results= 5) # n_results determina o numeros de resultados por pesquisa


            # implementa exibição de dados da recuperação em forma de texto formatado

               # print(results)

            # extrai os dados de cada chave e seu valor correspondente e armazena em uma lista de dicionários

                self.lista_dados_recuperados =[
                        {
                        "ids": id_,
                        "Distância": dist,
                        "textos":  doc,
                        "metadados": meta
                            }
                    
                    for id_, doc, dist, meta in zip(
                    results["ids"][0],
                    results["documents"][0],
                    results["distances"][0],
                    results["metadatas"][0],

                    )

                ]
                #print("\n")

                self.lista_completa_dados_recuperados.extend(self.lista_dados_recuperados)  

            for x, dados in enumerate(self.lista_completa_dados_recuperados):
                   print(f"dados recuperados {x}: \n {dados} \n")   

            return 1        


        else:

            self.lista_completa_dados_recuperados = ["Nenhum documento encontrado no banco de dados."]
            return 0


            # Comando para desligar o modelo específico instantaneamente

            subprocess.run(["ollama", "stop", "snowflake-arctic-embed2:568m"], check=True)
            print("Modelo descarregado da memória com sucesso!")





    def ordenação_de_dados(self):




        def similaridade_coseno():

            coseno = 0.65


            if self.lista_completa_dados_recuperados[0]["Distância"] <= coseno:
                print("O documento é relevante para a consulta.")

                return 1


            else: 
                #print("O documento não é relevante para a consulta.")

                return 0




        # ordena os dados recuperados com base na distância (menor distância indica maior relevância)

        self.lista_completa_dados_recuperados.sort(key=lambda x: x["Distância"])


        for x, dados in enumerate(self.lista_completa_dados_recuperados):
                
         print(f"dados recuperados ordenados {x}: \n {dados} \n")
         print(f"quantidade de documentos recuperados: {self.quantidade_de_documentos} \n")
         print(f"quantidade de dados recuperados: {len(self.lista_completa_dados_recuperados)} \n")

        sleep(10)


        if similaridade_coseno():



            #self.texto_formatado += "\n \n \n ".join([str(dado) for dado in self.lista_completa_dados_recuperados[:5]]) 
            
            for dados in self.lista_completa_dados_recuperados[:5]:

                self.texto_formatado  += f"\n\n\n documents\n  {dados.get('textos',None)} \n\n\n metadados \n { dados.get('metadados',None)}"
            
              
        else:
            self.texto_formatado = "Nenhum documento relevante encontrado para a consulta."


                    # Comando para desligar o modelo específico instantaneamente

        subprocess.run(["ollama", "stop", "snowflake-arctic-embed2:568m"], check=True)
        #print("Modelo descarregado da memória com sucesso!")
        return self.texto_formatado




            
