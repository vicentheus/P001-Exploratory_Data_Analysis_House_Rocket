# P001-Exploratory_Data_Analysis_House_Rocket
![house PNG](https://user-images.githubusercontent.com/95831942/149863245-524ea5ff-1655-4e41-aad6-575e26382197.png)

Este é um projeto fictício. A empresa, o contexto e as perguntas de negócios não são reais. Este portfólio está seguindo as recomendações do blog Seja um Data


​A logo criada é fictícia.

O projeto foi colocado em produção através do [Heroku] (https://project-analytics-hrocket.herokuapp.com/)


## 1. Descrição
A imobiliária House Rocket tem como modelo de negócio a comercialização de imóveis que sejam rentáveis,  para isso a  empresa busca novas oportunidades de compra. O CEO da House Rocket  deseja maximizar a receita da empresa buscando novas oportunidades de negócio. A melhor estratégia é a compra de casas em condições regulares e com boa localização  quando estiverem em baixa no mercado e vendê-las quando o mercado estiver em alta.  Assim, quanto maior a diferença entre a comprar e a venda, maior o lucro da companhia. 
O objetivo é propor recomendações para o negócio através de insights produzidos mediante Análise Exploratória de Dados .As questões a serem respondidas são:
1. Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?
2. Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?
Produto de dados solicitado:
- Dashboard interativo do portfólio disponível, com todas informações de negócio mais relevantes disponíveis atualmente, para que possam realizar análises.


---
## 2. Atributos
Os dados para este projeto podem ser encontrado em:https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885 . 
Abaixo segue a definição para cada um dos  atributos:
Variable | Definition
------------ | -------------
|id | Identification number of each property|
|date | The date when the property was available|
|price | The price of each property considered as the purchase price |
|bedrooms | Number of bedrooms|
|bathrooms | The number of bathrooms, the value .5 indicates a room with a toilet but no shower. The value .75 or 3/4 bathroom represents a bathroom that contains one sink, one toilet, and either a shower or a bath.|
|sqft_living | Square feet of the houses interior space|
|sqft_lot | Square feet of the houses land space |
|floors | Number of floors|
|waterfront | A dummy variable for whether the house was overlooking the waterfront or not, ‘1’ if the property has a waterfront, ‘0’ if not|
|view | An index from 0 to 4 of how good the view of the property was|
|condition | An index from 1 to 5 on the condition of the houses, 1 indicates worn-out property and 5 excellent|
|grade | An overall grade is given to the housing unit based on the King County grading system. The index from 1 to 13, where 1-3 falls short of building construction and design, 7 has an average level of construction and design, and 11-13 has a high-quality level of construction and design|
|sqft_above | The square feet of the interior housing space that is above ground level|
|sqft_basement | The square feet of the interior housing space that is below ground level|
|yr_built | Built year of the property |
|yr_renovated | Represents the year when the property was renovated. It considers the number ‘0’ to describe the properties never renovated.|
|zipcode | A five-digit code to indicate the area where the property is in|
|lat | Latitude|
|long | Longitude|
|sqft_living15 | The square feet average size of interior housing living space for the closest 15 houses|
|sqft_lot15 | The square feet average size of land lots for the closest 15 houses|


## 3. Premissas de Negócio

As seguintes premissas foram consideradas para esse projeto:
- Os valores iguais a zero em yr_renovated são casas que nunca foram reformadas.
-  O valor igual a 33 na coluna bathroom foi considerada um erro e por isso foi delatada das análises.
-  A coluna price significa o preço que a casa foi / será comprada pela empresa House Rocket.Valores duplicados em ID foram removidos e considerados somente a compra mais recente.
-  A localidade e a condição do imóvel foram características decisivas na compra ou não do imóvel.
-  A estação do ano foi a característica decisiva para a época da venda do imóvel.

* 3.1 Produto final

O que será entregue ?

Um grande dashboard interativo acessível via navegador, contendo os produtos de dados solicitados pelos times de negócio.

* 3.2 Ferramentas

Quais ferramentas serão usadas no processo?

* PyCharm;
* Jupyter Notebook;
* Git, Github;
* Python;
* Streamlit;
* Cloud Heroku.

## 4. Estratégia de soluçãe 
1. Coleta de dados via Kaggle
2. Entendimento de negócio
3. Tratamento de  de dados
* 3.1 Transformação
* 3.2 Limpeza
* 3.3 Entendiment
4. Exploração de dados
5. Resultados para o negócio
6. Conclusão

## 5. Top Data Insights
* H1: Imóveis com vista para água são em média 221,76% mais caros

* H5:  Como podemos observar, os imóveis que nunca sofreram reformas são em média 30% mais baratos. Essa comprovação pode sugerir a compra de imóveis nunca reformados que estão em ótimo estado.

* H6 e H7: Como observado, os imóveis sem porão são 89% maiores e 21,77% mais baratos em relação aos imóveis que possuem porão. Esse resultado sugere que é vantajoso a compra de imóveis sem porão que estão em bom/ótimo de conservação para a comercialização.

* H8 e H9 Imóveis com 6-9 quartos são mais caros sendo,149,56% mais caros se comparado a imóveis com 0 a 3 quartos, 48,94% mais caros se comparados a imóveis com 3 a 6 quartos e 107,25% mais caros se comparados a imóveis com 9 a 11 quartos.

## 6. Tradução para o negócio

Conforme o que foi definido, só foram sugeridos imóveis com ótimas condições para compra. 
Nesse sentido, todos  os imóveis apresentam condições de venda conforme a sazonalidade:

* Os imóveis com valor inferior ao preço médio pela região, terão um aumento de 30% no preço e serão vendidos.Mostrar na mesma tabela a melhor época para comprar e vender, com base no preço médio por região durante as temporadas
* Mostrar na mesma tabela a melhor época para comprar e vender, com base no preço médio por região durante as temporadas

De acordo com a margem estabelecida, algumas casas  excedem o preço da mediana da região.

Dessa maneira, é plausível  aumentar a margem, levando em consideração outros atributos do imóvel.

Levando em consideração apenas o lucro por imóvel,  caso a sugestão de compra e venda seja seguida o lucro total estimado  é de aproximadamente US$ 45 milhões dólares.

##  7. Conclusão

O objetivo do projeto foi alcançado, visto que os produtos de dados onde imóveis são recomendáveis ​​ou não para compra, considerando região, preço médio e temporada foram criados com êxito. Assim, o CEO da House Rocket, poderá utilizar a solução para tomada de decisão.

O dashboard com os produtos de dados em produção pode ser acessado via navegador pelo  [Heroku] (https://project-analytics-hrocket.herokuapp.com/)

## 8. Próximos passos

Algumas melhorias nos dashboard podem ser incrementadas no futuro:

*  Poderá ser feita uma análise para saber se é vantajoso reformar alguns imóveis e posteriormente vender, na intenção de aumentar o lucro.     

*  Analisar outras métricas e verificar a melhor ferramenta para solucionar o problema.
* Tentar prever a valorização dos imóveis além da sazonalidade.


**References:**
* Python from Zero to DS lessons on Meigarom channel [Youtube](https://www.youtube.com/watch?v=1xXK_z9M6yk&list=PLZlkyCIi8bMprZgBsFopRQMG_Kj1IA1WG&ab_channel=SejaUmDataScientist)
* Blog [Seja um Data Scientist](https://sejaumdatascientist.com/os-5-projetos-de-data-science-que-fara-o-recrutador-olhar-para-voce/)
* Dataset from [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction)
* Variables meaning on [Geocenter](https://geodacenter.github.io/data-and-lab/KingCounty-HouseSales2015/)
