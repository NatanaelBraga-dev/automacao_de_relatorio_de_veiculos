from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import pandas as pd 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
from datetime import datetime
from datetime import date
import re
from variaveisDeAmbiente import dadosColhidosPeloBot, baseDeVeiculos

driver = Chrome()

lista_multas = []
lista_resumo = []

caminho_arquivo = dadosColhidosPeloBot
df = pd.read_csv(baseDeVeiculos, sep=";").fillna("") #OBS: NO MEU CASO ESTOU USANDO UM CSV, SE ESSE NÃO FOR O SEU CASO, ADAPTE O CÓDIGO PARA UM .XLSX

driver.implicitly_wait(30)
driver.maximize_window()

#CONSULTA O VEÍCULO NA PÁGINA DO DETRAN INDICADA ABAIXO NA PARTE DE MULTAS
def ConsultarVeiculo(placa,renavam,cidade,estado, proprietario, centroCusto = None):
    driver.get("https://sistemas.detran.ce.gov.br/central") #página do detran
    action = ActionChains(driver=driver)
    driver.find_element(By.CSS_SELECTOR,'a[data-title="Licenciamento"]').click()

    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR,'div#panel-login-veiculo')

    driver.find_element(By.CSS_SELECTOR,'input#veiculo_placa').send_keys(placa)
    renavam_input = driver.find_element(By.CSS_SELECTOR, 'input#veiculo_renavam_chassi')
    renavam_input.send_keys(renavam, Keys.TAB, Keys.ENTER)
    time.sleep(1)

    try:
        localizandoDiv = driver.find_element(By.CSS_SELECTOR, 'div#div-form-veiculo-usado')
        validacaoVeiculo = localizandoDiv.find_element(By.CSS_SELECTOR, 'label.control-label')
        if validacaoVeiculo.text in ["Veículo não encontrado!", "inválida"]:
            print(f"O veículo que você está procurando não existe, placa: {placa}")
            print("Verifique se os dados estão corretos")
            return
    except:
        print("Elemento de validação não encontrado, seguindo o fluxo normal...")
        print(f"codigo de placa dentro do consultar veiculo {placa}")
        textoMultas = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-title="Veículo - Emissão de multas"]'))
            )
        
        if("Seu veículo não possui multas" not in textoMultas.text):
            time.sleep(1)
            qttdMultas = re.findall(r'\d+', driver.find_element(By.CSS_SELECTOR,'div[data-title="Veículo - Emissão de multas"]').text)
            print(f"quantidade de multas encontradas: {qttdMultas}")
            driver.find_element(By.CSS_SELECTOR,'div[data-title="Veículo - Emissão de multas"]').click()
            time.sleep(1)
            resultado = driver.find_element(By.CSS_SELECTOR,'div[data-title="Veículo - Emissão de multas"]').text
            time.sleep(1)
            print(f"numero da placa antes de getMultaInfo{placa}")
            getMultaInfo(placa,renavam,resultado,cidade, estado, proprietario, centroCusto, int(qttdMultas[0]))
            time.sleep(1)
        else:
            getVeiculoInfo(date.today(),placa, renavam,"Seu Veículo não possui multas", cidade, estado, proprietario, centroCusto, 0)
            pass

    action.perform()

#FUNÇÃO PARA PUXAR OS DADOS DO VEÍCULO, OBSERVE QUE ESSA FUNÇÃO APENAS PEGA OS DADOS QUE JÁ VEM DA BASE DE VEÍCULOS
def getVeiculoInfo(dataDeRegistro, placa, renavam,resultado, cidade, estado, proprietario, centroCusto, qttdMultas):
    print(f"codigo de placa dentro de getVeiculoInfo {placa}")

    dadosGeraisDeVeiculos = pd.DataFrame(
        {
            "date": [dataDeRegistro],
            "cod_placa": [placa],
            "codRenavam": [renavam],
            "resultado": [resultado],
            "cidade": [cidade],
            "estado": [estado],
            "proprietario": [proprietario],
            "centro_custo": [centroCusto],
            "quantidade_multas": [qttdMultas]
        }
    )
    time.sleep(1)
    lista_resumo.append(dadosGeraisDeVeiculos)
    print("adicionado a lista com sucesso!")

#FUNÇÃO PEGAR AS MULTAS
def getMultaInfo(placa, renavam, resultado, cidade, estado, proprietario, centroCusto, qttdMultas):
    print(f"placa dentro de getMultaInfo: {placa}")
    time.sleep(1)
    body = driver.find_element(By.TAG_NAME, "tbody")
    time.sleep(1)
    rows = body.find_elements(By.CSS_SELECTOR, "tr")
    
    for item in rows:
        print("coletando multas")
        informacoesListadas = item.find_elements(By.CSS_SELECTOR, "td")
        print(len(informacoesListadas))
        
        if len(informacoesListadas) != 8:
            break

        data_infracao = datetime.strptime(informacoesListadas[4].text.strip(), "%d/%m/%Y").date()
        data_vencimento = datetime.strptime(informacoesListadas[5].text.strip(), "%d/%m/%Y").date()
        print(f"codigo da placa antes de registrarMultaInfo {placa}")    
        registrarMultaInfo(date.today(),placa,renavam,informacoesListadas[1].text, informacoesListadas[2].text ,informacoesListadas[3].text,data_infracao,data_vencimento, informacoesListadas[6].text, informacoesListadas[7].text, cidade, estado, proprietario, centroCusto)
    print(f"codigo da placa antes de getVeiculoInfo {placa}")
    getVeiculoInfo(date.today(), placa, renavam, resultado, cidade, estado, proprietario, centroCusto, qttdMultas)
    time.sleep(1)

#FUNÇÃO PARA REGISTRO DE MULTAS
def registrarMultaInfo(dataDeRegistro, placa, renavam, AIT, AIToriginario , motivo, dataInfracao, dataVencimento, valor, valorAPagar, cidade, estado,proprietario, centroCusto):
    print(f"codigo de placa dentro de registrarMultaInfo")
    dadosMulta = pd.DataFrame(
        {
            "date": [dataDeRegistro],
            "cod_placa": [placa],
            "cod_renavam":[renavam],
            "AIT": AIT,
            "AIT_originario": [AIToriginario],
            "motivo": [motivo], 
            "data_infração": [dataInfracao],
            "data_vencimento": [dataVencimento],
            "valor": [valor],
            "valor_a_pagar": [valorAPagar],
            "cidade": [cidade], 
            "estado": [estado],
            "proprietario": [proprietario],
            "centro_custo": [centroCusto]
        }
    )
    lista_multas.append(dadosMulta)
    print("Dados de multa adicionados à lista.")

def limpar_placa(placa):
    # remove espaços, aspas e sinal de igual
    if isinstance(placa, str):
        return placa.strip().replace('"', "").replace("=", "")
    return placa

iteracao = df.iterrows()

for index, linhas in df.head(20).iterrows():  #ITERAÇÃO COM A PLANILHA DA BASE DE VEÍCULOS
    codigoPlaca = limpar_placa(linhas.cod_placa)
    codigoRenavam = int(linhas.cod_renavam)
    cidade = linhas.cidade
    proprietario = linhas.proprietario
    centroCusto = linhas.centro_custo
    estado = linhas.estado
    print(index, codigoPlaca, codigoRenavam)
    ConsultarVeiculo(codigoPlaca, codigoRenavam, cidade, estado, proprietario, centroCusto)

if lista_multas:  #AS LISTAS NÃO PODEM ESTAR VAZIAS SE NÃO CAUSARIA UM ERRO NO CONCAT
    df_multas_final = pd.concat(lista_multas, ignore_index=True)
else:
    df_multas_final = pd.DataFrame(columns=[
        "date", "cod_placa", "cod_renavam", "AIT", "AIT_originario", "motivo",
        "data_infração", "data_vencimento", "valor", "valor_a_pagar",
        "cidade", "estado", "proprietario", "centro_custo"
    ])

if lista_resumo:
    df_resumo_final = pd.concat(lista_resumo, ignore_index=True)
else:
    df_resumo_final = pd.DataFrame(columns=[
        "date", "cod_placa", "codRenavam", "resultado", "cidade", "estado",
        "proprietario", "centro_custo", "quantidade_multas"
    ])
#SALVA OS DADOS COLHIDOS E PARTE PARA E EXECUÇÃO DE ENVIO DE EMAIL
try:
    with pd.ExcelWriter(caminho_arquivo, engine='openpyxl') as writer:
        df_multas_final.to_excel(writer, sheet_name='multados', index=False)
        df_resumo_final.to_excel(writer, sheet_name='resumo', index=False)
    print(f"Dados salvos com sucesso no arquivo: {caminho_arquivo}")
    print("Partindo para o envio do email")
    try: 
        with open("emailBot.py") as f:
            exec(f.read())
    except Exception as e:
        print(f"ocorreu um durante a tentiva do envio do email {e}")
except Exception as e:
    print(f"Ocorreu um erro ao salvar o arquivo: {e}")
