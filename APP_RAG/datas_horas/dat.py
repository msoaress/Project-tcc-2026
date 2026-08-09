from datetime import datetime
class datas:

    def __init__(self):
          self.s= self
     





    def obter_data_hora_atual(self):
        agora = datetime.now()
        
        # Lista com os dias da semana
        dias_semana = [
            "Segunda-feira", "Terça-feira", "Quarta-feira", 
            "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"
        ]
        
        # agora.weekday() retorna 0 para Segunda, 1 para Terça, etc.
        dia_da_semana = dias_semana[agora.weekday()]
        
        # Formata a data e hora no padrão brasileiro (DD/MM/AAAA HH:MM:SS)
        data_hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")
        
        return  f"data_hora = {data_hora_formatada} e dia da semana = {dia_da_semana}"
       

