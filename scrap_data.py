# importando as bibliotecas necessarias
import requests
import csv

# para realizar uma solicitacao http precisamos informar um header, neste caso usaremos o user-agent
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0 (Edition std-1)'}

# criando uma lista para aumentar o alcance de retornos no scrap
label_search = ['estagio', 'analista', 'junior', 'jr' ,'pleno', 'pl', 'senior', 'sr']

# criando uma lista para definir o nome das colunas no arquivo csv
column_names = ['id', 'companyId', 'name', 'description', 'careerPageName', 'type', 'publishedDate', 'applicationDeadline', 'isRemoteWork', 'city', 'state', 'country', 'disabilities']

# lista vazia para salvar os dados
data = []

# conjunto para guardar os ids das vagas para impedir de gravar vagas repetidas
ids = set()


#aqui esta nosso scrap, faremos um HTTP GET no endpoint onde esta localizada as vagas, fazendo um busca por cada valor passado no rotulo anterior e salvando em um arquivo jobs.csv. 
with open('jobs.csv', 'a+', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    #aplicando nome nas colunas do csv
    writer.writerow(column_names)
    
    for label in label_search:
        url = f"https://portal.api.gupy.io/api/job?name={label}&offset=0&limit=10000"
        try:
            request = requests.get(url, headers=headers)
            request.raise_for_status()  
            #aqui convertemos os JSON em em um dict python
            data = request.json().get('data', [])
            
            for job in data:
                job_id = job.get('id', '')
                
                # Verificar se o id da vaga ja foi salvo
                if job_id not in ids:
                    ids.add(job_id)
                    
                    #dados que utilizaremos na nossa analise
                    row = [
                        job_id,
                        job.get('companyId', ''),
                        job.get('name', ''),
                        job.get('description', ''),
                        job.get('careerPageName', ''),
                        job.get('type', ''),
                        job.get('publishedDate', ''),
                        job.get('applicationDeadline', ''),
                        job.get('isRemoteWork', ''),
                        job.get('city', ''),
                        job.get('state', ''),
                        job.get('country', ''),
                        job.get('disabilities', ''),
                    ]
                    writer.writerow(row)
        #printando erro caso ocorra
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar dados para {label}: {e}")

print('ok')