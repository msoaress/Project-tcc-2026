import os
import streamlit as st
from groq import Groq

class chat_assistente:

    def __init__(self, dados_para_llm):

       self.dados_para_llm = dados_para_llm


    # modelos disponiveis

       self.modelos_locais =["llama-3.1-8b-instant"]
       self.api=st.secrets["api_key"]

       self.api=""





    def resposta_usuario(self):
       

        # configuração para enviar os dados para o llm


        client = Groq(
            api_key=self.api
        )

        #print(f"enviando dados para o modelo: {self.modelos_locais[0]}")

        response = client.chat.completions.create(
            model=self.modelos_locais[0],  # ex: "openai/gpt-oss-120b"
            messages=self.dados_para_llm,
            stream=True,
            temperature=0.7,         # Opcional (0.0 a 2.0)
            presence_penalty=0.5,    # Opcional (-2.0 a 2.0)
            max_tokens=1024,         # Opcional (substitui o 'num_predict')
        )
        

        return response
