import sys
import requests
from datetime import datetime, timedelta
from models import Session, Licitacoes, Datas

session = Session()

def get_licitacoes(period):
  api_url = f"http://nadic.ifrn.edu.br/api/dou/{period}/?usuario=dev_nadic"
  response = requests.get(api_url)
  lic = response.json()
  data = lic["licitacoes"]
  for i in range(len(data)):
    lici = Licitacoes(
      orgao = data[i]["orgao"],
      titulo = data[i]["titulo"],
      estado = data[i]["estado"],
      cidade = data[i]["cidade"],
      objeto = data[i]["objeto"]
      )   
    session.add(lici)
    session.commit()
    datas = data[i]["datas"]["Outras Datas"]
    for j in range(len(datas)):
      dat = Datas(
        licitacao_id = lici.id,
        label = datas[j]["label"],
        evento = datas[j]["evento"],
        orientacao = datas[j]["orientacao"],
        data = datas[j]["data"],
        fonte = datas[j]["fonte"],       
      )
      session.add(dat)
      session.commit()
  print(f"{period} finalizado")

if len(sys.argv) == 2:
  period = sys.argv[1]
  get_licitacoes(period)

else:
  d1 = sys.argv[1]
  d2 = sys.argv[2]

  first_date = datetime.strptime(d1, "%Y-%m-%d")
  second_date = datetime.strptime(d2, "%Y-%m-%d")

  days = abs((first_date - second_date).days) + 1
  period = d1
  for i in range(days):
      get_licitacoes(period)
      date = datetime.strptime(period, "%Y-%m-%d") + timedelta(days=1)
      period = datetime.strftime(date, "%Y-%m-%d" )
