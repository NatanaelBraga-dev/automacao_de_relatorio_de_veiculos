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
- ### Em breve terminarei o readme...