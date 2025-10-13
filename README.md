 ---
### **INSTRUÇÕES PARA UTILIZAR O PROJETO**
 ---

- ##### *CLONANDO O REPOSITÓRIO*
    Crie uma pasta para clonar o repositório, logo após clone o repositório dentro da sua pasta e acesse minha pasta de projeto.
    
```markdown
git clone https://github.com/NatanaelBraga-dev/Cadastro-e-Login-funcional.git
```

- ##### *CRIANDO UM AMBIENTE VIRTUAL E INSTALANDO AS BIBLIOTECAS*
Crie um ambiente virtual para instalar as bibliotecas.
```markdown
python -m venv venv
```
Entrando nas pastas do projeto
```
cd automacao_de_relatorio_de_veiculos
cd automacao
cd natan
```
Ativar o ambiente virtual e instalar as bibliotecas do projeto
```
venv/Scripts/Activate

pip install -r requirements.txt
```
Após isso, seu ambiente estará quase pronto para rodar o projeto

- #### *COMO DEVE SER O ARQUIVO CSV PARA LEITURA ?*
  - Como você deve ter visto, o código para funcionar precisa ler  um arquivo csv contendo os veículos que você quer percorrer.

```python
df = pd.read_csv(baseDeVeiculos, sep=";").fillna("") #OBS: NO MEU CASO ESTOU USANDO UM CSV, SE ESSE NÃO FOR O SEU CASO, ADAPTE O CÓDIGO PARA UM .XLSX

for index, linhas in df.head(20).iterrows():  #ITERAÇÃO COM A PLANILHA DA BASE DE VEÍCULOS
    codigoPlaca = limpar_placa(linhas.cod_placa)
    codigoRenavam = int(linhas.cod_renavam)
    cidade = linhas.cidade
    proprietario = linhas.proprietario
    centroCusto = linhas.centro_custo
    estado = linhas.estado
    print(index, codigoPlaca, codigoRenavam)
    ConsultarVeiculo(codigoPlaca, codigoRenavam, cidade, estado, proprietario, centroCusto)
```
- Como pode ver, é necessário se ter alguns dados para que o projeto funcione, como placa e renavam, como este projeto foi feito para uma corporação, tive que colocar outros campos a mais. se vc quiser você poder retirar-los dos dataframes e das funções, já que para buscar dados relacionados a multas ele não são necessarios.
<br>

- MODELO DE ARQUIVO PARA LEITURA:
  - Crie um arquivo excel chamado com as seguintes colunas:
    - cod_placa (obrigatório)
    - cod_renavam (obrigatório)
    - cidade (caso não queira utilizar isso, retire as linhas do código que utilizam isso)
    - proprietario (caso não queira utilizar isso, retire as linhas do código que utilizam isso)
    - centro_custo (caso não queira utilizar isso, retire as linhas do código que utilizam isso)
    - estado (caso não queira utilizar isso, retire as linhas do código que utilizam isso)
<br>
  - Depois disso, salve o arquivo como csv para que os dados sejam lidos corretamente, caso contrário se forem salvos como xlsx será preciso alterar a forma como o arquivo é lido.
  <br>
  - Crie também um arquivo chamado ```dadosColhidosPeloBot```, que será o arquivo que o pandas vai manipular para realizar o relatório dos dados colhidos. ``obs: esse pode ser .xlsx``
  <br>
  - Após isso, crie uma pasta chamada ``baseDeDados`` dentro da pasta ``natan`` e coloque o arquivo de leitura e o arquivo ```dadosColhidosPeloBot``` dentro de ``baseDeDados``,<br> ``obs: se você quiser, você pode substituir ou renomear essa pasta "natan", desde que faça as alterações no código, ele vai funcionar corretamente``.
  <br>
  - Crie um arquivo chamado ``variaveisDeAmbiente`` e dentro desse arquivo crie variaveis para armazenar os caminhos do arquivo de leitura e do arquivo que o pandas vai manipular
  <br>

Ex:   
  ```python
  dadosColhidosPeloBot = "C:/Users/seuUsuario/projetos/robo_detran/automacao/natan/baseDeDados/dadosColhidosPeloBot.xlsx"
  baseDeVeiculos =  "C:/Users/seuUsuario/projetos/robo_detran/automacao/natan/baseDeDados/seuArquivoDeLeitura.csv"
  ```

logo após isso, se no seu arquivo bot.py estiver importando esses dados, estará tudo correto para execução dessa parte, caso não deseje enviar e-mails com esse relatório, você já está apto a rodar o projeto.


### ENVIO DE EMAILS

- Dentro do arquivo emailBot.py ao realizar a conexão com SMPT
```python
#CONEXÃO COM SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587 
USERNAME = username
PASSWORD = password
```

- Note que é necéssário ter configurado antes os valores do seu username, que nesse caso é o seu email que previamente deve estar configurado para que seja autorizado o envio de emails utilizando SMTP através dele, e logo após vai precisar da sua senha de acesso que será uma senha de aplicativo.
<br>
- Essa senha de aplicativo é uma configuração especifica que você precisa fazer para que o google permita o acesso da biblioteca a essa conta.
<br>

- ##### Caso não saiba fazer a configuração acesse:
  ```
  https://mailtrap.io/pt/blog/gmail-smtp/#Como-configurar-o-servidor-SMTP-do-Gmail

  https://youtu.be/TrdWr3BmqT8?si=smjr3vdhZiczSVAA
  ```

- Quando sua configuração de conta e SMTP estiver pronta, adicione as variaveis username e password no arquivo variaveisDeAmbiente.py e importe esses valores dentro do arquivo emailBot.py e importe tambem ``dadosColhidosPeloBot``
```python
from variaveisDeAmbiente import username, password, dadosColhidosPeloBot
```
<br>

- Após isso, basta seguir os passos que já estão comentados no próprio código para finalizar a configuração, como por exemplo os emails dos receptores.