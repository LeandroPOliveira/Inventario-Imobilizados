# Inventário de imobilizados / Assets Inventory

Modelo preliminar

Aplicativo para facilitar o trabalho de campo de identificação de imobilizados com número de plaqueta, sejam móveis, equipamentos etc...

Utilizando uma base inicial extraida do sistema SAP para alimentar o aplicativo através de criação de banco de dados simples do Sqlite, podemos fazer uma seleção dos ativos através de data de imobilização, descrição ou número de inventário.<br> 
Para inclusão dos números das plaquetas podemos digitar ou utilizar o reconhecimento de voz*, a fim de agilizar o processo em campo.

\* O sistema android ainda não possui uma "receita" para o pacote do Python Voice Recognition, impossibilitando o uso do reconhecimento de voz em aparelhos celulares.

---

Preliminary model

App made to facilitate the field work for assets identification with a plate number, such as furniture, equipments etc...

Using a initial database extracted from SAP system for feed the app towards the criation of a simple database from Sqlite, we can make a selection of the assets throught the activation date, description or inventory number.
For the inclusion of plate numbers we can type or use the voice recognition*, in order to speed up the field work.

\* Android doesn't have a recipe for the library Voice Recognition from python yet, so it only works on a computer, not on a mobile device.


Tela de Pesquisa / Search Screen:

<a href="url"><img src="https://github.com/LeandroPOliveira/Reconhecimento-voz/blob/main/Tela_app.gif" align="left" height="600" width="350" ></a><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>


Após finalizar os trabalhos, poderá ser gerado um script para retornar os dados para o sistema SAP de forma automática, através da data do trabalho realizado, eliminando trabalhos manuais.
 
---

After the work is done, you can generate a script to return the data for the SAP system automaticaly, throught the date of the work executed, eliminating manual work.
 
 Tela exportação Script SAP / SAP Script export:<br>
 
 <a href="url"><img src="https://github.com/LeandroPOliveira/Reconhecimento-voz/blob/main/Tela_exportacao.png" align="left" height="600" width="350" ></a><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>

Script em execução / Script being executed:<br>

<a href="url"><img src="https://github.com/LeandroPOliveira/Reconhecimento-voz/blob/main/Script_Sap.gif" align="left" height="500" width="450" ></a>

