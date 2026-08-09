# importação de bibliotecas e modulos necessários para o funcionamento do aplicativo, incluindo a configuração do prompt, a interface do usuário com Streamlit, a execução de comandos do sistema, a busca vetorial e a interação com o modelo de linguagem para gerar respostas ao usuário.
import sys
import os
from pathlib import Path

# Garante que o Python consiga encontrar arquivos na raiz do projeto
RAIZ = Path(__file__).resolve().parent.parent.parent
if str(RAIZ) not in sys.path:
    sys.path.append(str(RAIZ))

# Agora você importa direto do arquivo 'config.py'
from configuracao_de_caminhos.config_path import PASTA_IMAGENS
# Adiciona a pasta raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))



import APP_.prompt.conf_prompt as conf_prompt
import streamlit as st
import subprocess
import os
import APP_.busca_vetorial.busca_vetorial as busca_vetorial 
from APP_.Rag.llm_resposta_usuario import chat_assistente
from APP_.datas_horas.dat import datas


# variaveis globais
modelos_locais =["llama3.1:8b"]
prompt = None
response = None
resp = ""
conteudo = None
historico_assistente = "respostas do assistente:\n"
os.system("clear")



# variaveis globais com persistência


if "interacao" not in st.session_state:
     st.session_state.interacao = 0


if "dados_para_llm" not in st.session_state:
     # passagem de informações do prompt para a configuração do assistente

    app  = conf_prompt.configuracao()
    personaConfig = app.extracao_prompt()
    #print(f"Texto do prompt: {texto}")  
    st.session_state.dados_para_llm = [{"role":"system","content":personaConfig}] # todo chave rule, user, system, assistant e content nuca deveram ter espaços em branco entre ela e as aspas ex: "role ", "role " ou " role ", isso e valido para todos e valido a logica de chave valor.

if "historico_de_perguntas_do_usuario_e_respostas_do_asssistente" not in st.session_state:
     st.session_state.historico_de_perguntas_do_usuario_e_respostas_do_asssistente =""



if "historico_assistente" not in st.session_state:
     st.session_state.historico_assistente =""

     
# configurações da pagina do meu app

st.set_page_config(
    page_title="AI Assistant front end",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# __________________________________________barra lateral___________________________________________________________



# imagem logo lnls e imagem decorativa da barra lateral

with st.sidebar:
    with st.sidebar.container(horizontal_alignment="center",height= 250,border=False):
            st.image(str(PASTA_IMAGENS / "ChatGPT Image 8 de ago. de 2026, 17_26_16.png"), width=300)


# imagem logo flor de paineira  decorativa da barra lateral
with st.sidebar:
    with st.sidebar.container(vertical_alignment="center",height= 425,border=False):
          st.image(str(PASTA_IMAGENS / "inteligencia-artificial.jpg"), width= 400)
         
         # cabeçalho da barra lateral 
          st.sidebar.header(":green[Application Options]", text_alignment='center')
          
          # aguarda usuario clicar no botão novo chat para lipar a tela e iniciar uma nova conversa

          if st.sidebar.button(":red[New Chat]", icon='✅',use_container_width=True,type='secondary'):
           

           

           
            #print("Modelo descarregado da memória com sucesso!")

           
  
            st.session_state.interacao = 0
            response =response = None
            conteudo = None
            resp = ""
            prompt = None
            app  = conf_prompt.configuracao()
            personaConfig = app.extracao_prompt()
            st.session_state.historico_assistente = ""
            st.session_state.historico_de_perguntas_do_usuario_e_respostas_do_asssistente =""

            st.session_state.dados_para_llm = [{"role":"system","content":personaConfig}] # todo chave rule, user, system, assistant e content nuca deveram ter espaços em branco entre ela e as aspas ex: "role ", "role " ou " role ", isso e valido para todos e valido a logica de chave valor.


        # texto para o rodapé da barra lateral
           
#""" st.sidebar.space(2)
      #    st.sidebar.link_button(label = ':violet[official website paineira] ',url ='https://lnls.cnpem.br/#facilities/paineira/',width = 'stretch',type='secondary',icon = '🌐')"""



#___________________________________________________________interface principal___________________________________________________________



# cria o titulo para a minha pagina


# opção para ecolher o modelo

#with st.container(horizontal=True, horizontal_alignment="left",):
   # st.selectbox("Available models", [modelo for modelo in modelos_locais],width= 200)

st.title(':blue[AI Assistant] :green[🚀]', text_alignment= 'center')
st.space(10)


# aguardo o usuario digitar e clicar em enviar para processar a resposta

 
prompt = st.chat_input('Digite algo')   # cria um caixa de texto para o ususario digitar algo

#st.markdown(st.session_state.historico_de_perguntas_do_usuario_e_respostas_do_asssistente)

if prompt is not None:

# exibe o historico de perguntas e respostas 
       
     
     with st.container(height=400, border=True, autoscroll=True):
        with st.chat_message("user",avatar=(str(PASTA_IMAGENS / "capybara-wearing-sunglasses.png"))):


                if  st.session_state.interacao >0: 
                 
                 st.session_state.historico_de_perguntas_do_usuario_e_respostas_do_asssistente += f"respostas do assistente:\n\n{st.session_state.historico_assistente}"

        st.session_state.historico_de_perguntas_do_usuario_e_respostas_do_asssistente += f"\n \n\n\n\n sua pergunta:\n\n{prompt}\n\n\n\n\n"
      
        if  st.session_state.interacao >0:
         st.markdown(st.session_state.historico_de_perguntas_do_usuario_e_respostas_do_asssistente)
     st.space(50)

     with st.chat_message('human'):


        st.markdown('<br>' , text_alignment='left',width= 1400,unsafe_allow_html=True) 
        st.markdown(prompt, text_alignment='left',width= 1300)

        # Limpar a barro de assistente.
        response =response = None
        conteudo = None
        resp = ""

# apagar a memoria apos n interações

        st.session_state.interacao += 1
    
        if st.session_state.interacao == 10:

                #print(f"\n\nvalores:{st.session_state.interacao}\n\n")     
                st.session_state.interacao = 0
                response =response = None
                conteudo = None
                resp = ""
                prompt = None
                app  = conf_prompt.configuracao()
                personaConfig = app.extracao_prompt()
                st.session_state.historico_de_perguntas_do_usuario_e_respostas_do_asssistente =""
                st.session_state.historico_assistente = ""
                st.session_state.dados_para_llm = [{"role":"system","content":personaConfig}] # todo chave rule, user, system, assistant e content nuca deveram ter espaços em branco entre ela e as aspas ex: "role ", "role " ou " role ", isso e valido para todos e valido a logica de chave valor.
                st.rerun()

# inserir o icone do assistente na interface

        with st.chat_message("assistant"):
                placeholder = st.empty()
                placeholder.markdown(":shimmer[Gerando resposta...]")
        
        #implementação da camada de recuperação

                db = busca_vetorial.BuscaVetorial(prompt)
                if db.recuperar_informacao():
                        recupera_informacao_db_vetorial = db.ordenação_de_dados()
                # print(f"informação recuperada: \n {recupera_informacao} \n")


                else: 
                
                        recupera_informacao_db_vetorial = db.lista_completa_dados_recuperados
                #print("sem dados")
        


                # pega hora, data locais

                data = datas()
                dados = data.obter_data_hora_atual()




                                                        
        # envio de dados para o llm
                

                st.session_state.dados_para_llm.append({
                        "role":"user",  # todo chave rule, user, system, assistant e content nuca deveram ter espaços em branco entre ela e as aspas ex: "role ", "role " ou " role ", isso e valido para todos e valido a logica de chave valor.
                        "content":(
                                "### CONTEXTO DE RECUPERAÇÃO (RAG) ###\n"
                                f"{recupera_informacao_db_vetorial}\n\n"
                                f"{dados}"                         "-------------------------\n"
                                "### PERGUNTA DO USUÁRIO ###\n"
                                f"\n{prompt}"
                                )
                                })                                                                                             
    
        
        
                # configuração para enviar os dados para o llm

                app_1 = chat_assistente(st.session_state.dados_para_llm)

          # envia os dados para o modelo

                #print(f"enviando dados para o modelo: {modelos_locais[0]}")
                response = app_1.resposta_usuario()


                # implementação para que o modelo gerar a resposta para o usuario            
  

                if response is not None:
                         
                 message_placeholder = st.empty()  # criada aqui dentro
                 for resposta in response:            
                   conteudo = resposta.choices[0].delta.content or "" 
                   resp += conteudo
                   message_placeholder.markdown(resp + "▌")  # cursor piscante
                   placeholder.markdown("")

                 message_placeholder.markdown(resp)  # exibe o texto final sem cursor
                


        # Atualiza histórico do modelo

                historico_assistente = resp
                st.session_state.historico_assistente = resp
        
                st.session_state.dados_para_llm.append({"role":"assistant","content":historico_assistente})# todo chave rule, user, system, assistant e content nuca deveram ter espaços em branco entre ela e as aspas ex: "role ", "role " ou " role ", isso e valido para todos e valido a logica de chave valor.


                #for lista in st.session_state.dados_para_llm:

                  #print(f"lista com  dados: \n {lista}\n fim da lista \n")

