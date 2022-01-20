import streamlit as st
import geopandas
import pandas as pd
import numpy  as np
import folium
import plotly.express as px


from PIL import Image

from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

from datetime import datetime

st.set_page_config( layout='wide' )

image=Image.open('house.PNG.png')
st.sidebar.image(image,use_column_width=True)

st.markdown('''# Problema de Negócios
A imobiliária House Rocket tem como modelo de negócio a comercialização de imóveis que sejam rentáveis,  
para isso a  empresa busca novas oportunidades de compra. O CEO da House Rocket  deseja maximizar a 
receita da empresa buscando novas oportunidades de negócio. A melhor estratégia é a compra de casas em 
condições regulares e com boa localização  quando estiverem em baixa no mercado e vendê-las quando o 
mercado estiver em alta. Assim, quanto maior a diferença entre a comprar e a venda, maior o lucro da companhia. 
Serão definidas aqui abaixo algumas hipóteses e vou descobrir se essas hipóteses são Verdadeiras ou não.

#### Objetivo principal:
- Maximize a receita da empresa encontrando boas oportunidades de negócios.


#### Perguntas:
- Quais casas o CEO da House Rocket deve comprar e a que preço de compra?
- Uma vez que a casa é propriedade da empresa, qual o melhor momento para vendê-la e qual seria o preço de venda?
- A House Rocket deve fazer uma reforma para aumentar o preço de venda? Quais seriam as sugestões de mudanças? Qual é o aumento de preço dado para cada opção de reforma?
#### Abordagem da solução:
- Apresentar uma tabela que contenha o valor adquirido e o preço que deverá ser vendido. 
- Sabendo que o preço pode ser afetado pela localização (que é o recurso "CEP") e época do ano. 
#### Estratégia:
- Compre boas casas em ótimas localizações a preços baixos e depois revenda-as mais tarde a preços mais altos.
- A sugestão vai ser: 
 - Os imóveis com valor inferior ao preço médio por região, terão um aumento de 30% no preço e serão vendidas. 
 - Mostrar na mesma tabela a melhor época para comprar e vender, com base no preço médio por região durante as temporadas
#### Hipóteses:
- H1: Imóveis que possuem vista para água, são 30% mais caros, na média.
- H2: imóveis que possuem 3 quartos , são 50% mais baratos, na média.
- H3: Imóveis com data de construção menor que 1955, são 50% mais baratos, na média.
- H4: Imóveis com data de reforma maior que 2000, são 30% mais caros, na média.
- H5: Imóveis que nunca foram reformados são em média 40% mais baratos
- H6: Imóveis sem porão possuem área total 50% maiores que os imóveis com porão.
- H7: Imóveis sem porao, são 20% mais baratos, em média.
- H8: Imóveis com mais banheiros são em média 20% mais caros.
- H9: Imóveis com mais quartos são em média 20% mais caros.
''')
st.header('Contato')
st.write("For more information verify on: "
             "[GitHub](https://github.com/vicentheus)")

st.write("Made by **Vicente Matheus da Silva Santos**"
             " \n\n"
             "Social media: [LinkedIn](https://www.linkedin.com/in/vicente-matheus-77b012170/) "
             "  [Mail](vicent-matheus@hotmail.com)")


@st.cache( allow_output_mutation=True )
def get_data( path ):
    data = pd.read_csv( path )

    return data


@st.cache( allow_output_mutation=True )
def get_geofile( url ):
    geofile = geopandas.read_file( url )

    return geofile

def set_feature( data ):
    data['price_m2'] = data['price'] / data['sqft_lot']

    # Removendo os ID que estão duplicados, considerando somente os valores mais recente
    data = data.sort_values('date', ascending=False).drop_duplicates(subset='id', keep='first')

    # removendo o imóveis que possui 33 quartos por ser um outlier
    data = data.drop(15870)

    return data

def overview_data( data ):

    st.sidebar.title('General Data Options')
    st.title('Data Overview')

    f_attributes = st.sidebar.multiselect('Enter columns', data.columns)
    f_zipcode = st.sidebar.multiselect('Enter zipcode', data['zipcode'].unique())


    if (f_zipcode != []) & (f_attributes != []):
        data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]

    elif (f_zipcode != []) & (f_attributes == []):
        data = data.loc[data['zipcode'].isin(f_zipcode), :]

    elif (f_zipcode == []) & (f_attributes != []):
        data = data.loc[:, f_attributes]

    else:
        data = data.copy()

    # Average metrics
    if (all([x in f_attributes for x in ['id', 'zipcode', 'price', 'price_m2', 'sqft_living']]) == True) | (
            f_attributes == []):

        c1, c2 = st.columns((1, 1))

        # Average metrics
        df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
        df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
        df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
        df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

        df5 = pd.merge(df1, df2, on='zipcode', how='inner')
        df6 = pd.merge(df5, df3, on='zipcode', how='inner')
        df = pd.merge(df6, df4, on='zipcode', how='inner')
        df.columns = ['ZIPCODE', 'TOTAL HOUSES', 'PRICE', 'SQRT LIVING', 'PRICe/M2']

        c1.header('Average Values')
        c2.header('Descriptive Analysis')

        #c1.header('Average Values')
        #c1.dataframe(df, height=600)

        c1.write('''Here it's showed, The average price per regions(zipcode). We're able to see
        what regions are more expensive than others **(you're able to sort the DataFrame pressing over the name the feature you want to sort)**,
        and what's the maximum and minimum average price per regions
        and find out what regions are cheaper or more expensive. Together with this information you'll be able
        to filter using this interested regions to filter the dataset and make your analysis''')

        c2.write('''Here it's showed some descriptive statistics that might be important to make or base decisions''')
        df_aux = data.describe().T[['mean', '50%', 'min', 'max', 'std']]
        df_aux.columns = ['Mean', 'Median', 'Min', 'Max', 'Std']

        c1.dataframe(df, height=400)
        c2.dataframe(df_aux, height=400)

    else:
        st.write('If you want to be able to see the **STATISTICS ANALYSIS** select at least that columns: \n\n **{}**'.format(
        ['id', 'zipcode', 'price', 'price_m2', 'sqft_living']))

    # statistic descriptive
    num_attributes = data.select_dtypes(include=['int64', 'float64'])
    media = pd.DataFrame(num_attributes.apply(np.mean))
    mediana = pd.DataFrame(num_attributes.apply(np.median))
    std = pd.DataFrame(num_attributes.apply(np.std))

    max_ = pd.DataFrame(num_attributes.apply(np.max))
    min_ = pd.DataFrame(num_attributes.apply(np.min))

    df1 = pd.concat([max_, min_, media, mediana, std],
                    axis=1).reset_index()

    df1.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std']

    c2.header('Descriptive Analysis')
    c2.dataframe(df1, height=800)

    return None

def portfolio_density(data, geofile):

    st.title('Region Overview')

    c1, c2 = st.columns((1, 1))
    c1.header('Portfolio Density')

    df = data.sample(10)

    # Base Map - Folium
    density_map = folium.Map(location=[data['lat'].mean(),
                                       data['long'].mean()],
                             default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in df.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Sold R${0} on: {1}. Features: {2} sqft, {3} bedrooms,{4} bathrooms, year built: {5}'.format(
                          row['price'],
                          row['date'],
                          row['sqft_living'],
                          row['bedrooms'],
                          row['bathrooms'],
                          row['yr_built'])).add_to(marker_cluster)

    with c1:
        folium_static(density_map)

    # Region Price Map
    c2.header('Price Density')

    df = data[['price',
               'zipcode']].groupby('zipcode').mean().reset_index()
    df.columns = ['ZIP', 'PRICE']

    # df = df.sample( 10 )

    geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]

    region_price_map = folium.Map(location=[data['lat'].mean(),
                                            data['long'].mean()],
                                  default_zoom_start=15)

    region_price_map.choropleth(data=df,
                                geo_data=geofile,
                                columns=['ZIP', 'PRICE'],
                                key_on='feature.properties.ZIP',
                                fill_color='YlOrRd',
                                fill_opacity=0.7,
                                line_opacity=0.2,
                                legend_name='AVG PRICE')

    with c2:
        folium_static(region_price_map)

    return None
def     commercial_distribution( data ):
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    # --------Average Price per Year
    st.header('Average Price per Year built')

    # filter
    min_year_built = int(data['yr_built'].min())
    max_year_built = int(data['yr_built'].max())
    median_year_built = int(data['yr_built'].median())

    st.sidebar.subheader('Select Max Year Built')
    f_year_built = st.sidebar.slider(
        'Year Built', min_year_built, max_year_built, median_year_built)

    # data selection
    df = data.loc[data['yr_built'] < f_year_built]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    # plot
    fig = px.line(df, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # -------- Average Price per Day

    st.header('Average Price per Day')

    st.sidebar.subheader('Select Max Date')

    # filters
    min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
    max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')

    f_date = st.sidebar.slider('Date', min_date, max_date, max_date)

    # data Select
    data['date'] = pd.to_datetime(data['date'])
    df = data.loc[data['date'] < f_date]
    df = df[['date', 'price']].groupby('date').mean().reset_index()

    # plot
    fig = px.line(df, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # -------- Histograma

    st.header('Price Distribution')
    st.sidebar.subheader('Select Max Price')

    # filter
    min_price = int(data['price'].min())
    max_price = int(data['price'].max())
    median_price = int(data['price'].median())

    # data filtering
    f_price = st.sidebar.slider('price', min_price, max_price, median_price)
    df = data.loc[data['price'] < f_price]

    # data plot
    fig = px.histogram(df, x='price', nbins=50)
    st.plotly_chart(fig, use_container_width=True)

    return data


def      attributes_distribution( data ):

    st.sidebar.title('Attributes OPtions')
    st.title('House Attributes')

    # filters
    f_bedrooms = st.sidebar.selectbox('Max number of bedrooms', sorted(set(data['bedrooms'].unique())))

    f_bathrooms = st.sidebar.selectbox('Max number of bathrooms', sorted(set(data['bathrooms'].unique())))

    c1, c2 = st.columns(2)

    # Houses per bedrooms
    c1.header('House per bedrooms')
    df = data[data['bedrooms'] < f_bedrooms]
    fig = px.histogram(data, x='bedrooms', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # House per bathrooms
    c2.header('House per bathrooms')
    df = data[data['bathrooms'] < f_bathrooms]
    fig = px.histogram(data, x='bathrooms', nbins=19)
    c2.plotly_chart(fig, use_container_width=True)

    # filters
    f_floors = st.sidebar.selectbox('MAx number of floor', sorted(set(data['floors'].unique())))

    f_waterview = st.sidebar.checkbox('Only House with Water View')

    c1, c2 = st.columns(2)

    # Houses per floors
    c1.header('Houses per floors')
    df = data[data['floors'] < f_floors]
    fig = px.histogram(df, x='floors', nbins=19)
    c1.plotly_chart(fig, use_containder_width=True)

    # House per water view

    if f_waterview:
        df = data[data['waterfront'] == 1]
    else:
        df = data.copy()

    # plot
    fig = px.histogram(df, x='waterfront', nbins=10)
    c2.header('Houses per water view')
    c2.plotly_chart(fig, use_containder_width=True)

    return data

def hipoteses (data):

    # =========================================
    # ========== H1 ===========================
    # ==========================================

    st.markdown("<h1 style='text-align: center; color: black;'>Testando Hipóteses de Negócio</h1>",unsafe_allow_html=True)
    st.write( 'Nessa seção iremos verificar a veracidade da hipótese criada com intuito descobrir novas oportunidades de negocio para a empresa.')
    c1, c2 = st.columns(2)

    c1.subheader('Hipótese 1:  Imóveis com vista para a água são em média 30% mais caros')
    c1.write('Falsa. Imóveis com a vista para a água são 211.76% mais caros.')
    data[['price', 'waterfront', 'sqft_lot']].groupby('waterfront').mean().reset_index()
    h1 = data[['price', 'waterfront', 'sqft_lot']].groupby('waterfront').mean().reset_index()
    h1['waterfront'] = h1['waterfront'].astype(str)
    fig = px.bar(h1, x='waterfront', y='price', color='waterfront', labels={"waterfront": "Visão para água",
                                                                            "price": "Preço"}, template='simple_white')

    fig.update_layout(showlegend=False)
    c1.plotly_chart(fig, use_container_width=True)

    # =========================================
    # ========== H2 ==========
    # ==========================================

    c2.subheader('Hipótese 2: imóveis que possuem 2 quartos , são 50% mais baratos, em relação a imóveis de 4 quartos.')
    c2.write('Falsa. Imóveis que possuem 2 quartos, são 36.77% mais baratos em relação aos imoveis de 4 quartos..')
    data['dormitory_type'] = 'other'
    data.loc[data['bedrooms'] == 0, 'dormitory_type'] = 'NA'
    data.loc[data['bedrooms'] == 1, 'dormitory_type'] = 'bedrooms_1'
    data.loc[data['bedrooms'] == 2, 'dormitory_type'] = 'bedrooms_2'
    data.loc[data['bedrooms'] == 3, 'dormitory_type'] = 'bedrooms_3'
    data.loc[data['bedrooms'] == 4, 'dormitory_type'] = 'bedrooms_4'
    data.loc[data['bedrooms'] >= 5, 'dormitory_type'] = 'other'
    h2 = data[['price', 'dormitory_type', 'bedrooms']].groupby('dormitory_type').mean().reset_index()
    data[['price', 'dormitory_type', 'bedrooms']].groupby('dormitory_type').mean().reset_index()

    fig2 = px.bar(h2, x='dormitory_type', y='price', color='dormitory_type',
                  labels={"dormitory_type": "tipos de dormitórios",
                          'price': 'preço dos quartos'}, template='simple_white')

    fig2.update_layout(showlegend=False)
    c2.plotly_chart(fig2, use_container_width=True)

    # =========================================
    # ========== H3 ==========
    # ==========================================
    c3, c4 = st.columns(2)

    c3.subheader('Hipótese 3: Imóveis com data de construção menor que 1955, são 50% mais baratos, na média.')
    c3.write('Falsa. Imóveis com data de construção menor que 1955 são, 1.40% mais caros.')
    data['construcao'] = data['yr_built'].apply(lambda x: '> 1955' if x > 1955 else '<1955')
    data[['construcao', 'price', 'sqft_lot']].groupby('construcao').mean().reset_index()

    h3 = data[['construcao', 'price', 'sqft_lot']].groupby('construcao').mean().reset_index()
    fig3 = px.bar(h3, x='construcao', y='price', color='construcao', labels={'price': 'Preço',
                                                                             'sqm_lot': 'Área Total'},
                  template='simple_white')
    fig3.update_layout(showlegend=False)
    c3.plotly_chart(fig3, use_container_width=True)

    # =========================================
    # ========== H4 ==========
    # ==========================================
    c4.subheader('Hipótese 4: Imóveis com data de reforma maior que 2000, são 30% mais caros, na média.')
    c4.write('Falsa. Imóveis com data de reforma maior que 2000 são, 52.61% mais caros.')
    data['reforma'] = data['yr_renovated'].apply(lambda x: '>2000' if x > 2000 else '<2000')
    h4 = data[['reforma', 'price', 'sqft_lot']].groupby('reforma').mean().reset_index()
    fig4 = px.bar(h4, x='reforma', y='price', color='reforma', labels={'reforma': 'reforma',
                                                                       'price': 'Preço'}, template='simple_white')
    fig4.update_layout(showlegend=False)
    c4.plotly_chart(fig4, use_container_width=True)

    # =========================================
    # ========== H5 ==========
    # ==========================================
    c5, c6 = st.columns(2)
    c5.subheader('Hipótese 5: Imóveis que nunca foram reformados são em média 40% mais baratos')
    c5.write(' Verdadeira. Imóveis que nunca foram reformados são em média 43.29% mais baratos em relação aos imóveis que ja sofreram algum tipo de reforma.')
    data['renovacao'] = data['yr_renovated'].apply(lambda x: 'sim' if x > 0 else 'não')

    h5 = data[['renovacao', 'price']].groupby('renovacao').mean().reset_index()
    fig5 = px.bar(h5, x='renovacao', y='price', color='renovacao', labels={'price': 'Preço', 'renovacao': 'Quantidade de casas reformadas'}, template='simple_white')
    fig5.update_layout(showlegend=False)
    c5.plotly_chart(fig5, use_container_width=True)

    # =========================================
    # ========== H6 ==========
    # ==========================================
    c6.subheader('Hipótese 6: Imóveis sem porão possuem área total 50% maiores que os imóveis com porão.')
    c6.write('verdadeira. Imóveis sem porão são, 89.78% maiores em relação aos imóveis com porão.')
    data['porao'] = data['sqft_basement'].apply(lambda x: 'não' if x == 0 else 'sim')
    h6 = data[['porao', 'sqft_lot', 'price']].groupby('porao').sum().reset_index()
    fig6 = px.bar(h6, x='porao', y='sqft_lot', color='porao', labels={'porao': 'porao', 'sqft_lot': 'tamanho das casas'}, template='simple_white')

    fig6.update_layout(showlegend=False)
    c6.plotly_chart(fig6, use_container_width=True)

    # =========================================
    # ========== H7 ==========
    # ==========================================

    c1, c2 = st.columns(2)

    c1.subheader('Hipótese 7:Imóveis sem porao, são 20% mais baratos, em média.')
    c1.write('Verdadeira. Imóveis sem porão são, 20.99% mais baratos em relação aos imóveis com porão.')
    data['porao'] = data['sqft_basement'].apply(lambda x: 'não' if x == 0 else 'sim')
    data[['porao', 'sqft_lot', 'price']].groupby('porao').mean().reset_index()
    h7 = data[['porao', 'sqft_lot', 'price']].groupby('porao').mean().reset_index()

    fig7 = px.bar(h7, x='porao', y='price', color='porao',
                  labels={'porao': 'porao', 'price': 'preço dos imóveis'}, template='simple_white')

    fig7.update_layout(showlegend=False)
    c1.plotly_chart(fig7, use_container_width=True)

    # =========================================
    # ========== H8 ==========
    # ==========================================
    c2.subheader('Hipótese 8:Imóveis com mais banheiros são em média 20% mais caros')
    c2.write('Falsa. Os imóveis com 3 a 5 banheiros são,119.70% mais caros que imoveis com 0 a 3 banheiros, e imóveis com 3 a 5 banheiros são,27.74%  mais caros que imóveis com 5 a 8 banheiros.')
    data['banheiro'] = data['bathrooms'].apply( lambda x: '0-3' if (x > 0) & (x < 3) else '3-5' if (x > 3) & (x < 5) else '5-8')
    data[['banheiro', 'price']].groupby('banheiro').mean().reset_index()
    h8 = data[['banheiro', 'price']].groupby('banheiro').mean().reset_index()
    fig8 = px.bar(h8, x='banheiro', y='price', color='banheiro', labels={'price': 'Preço', 'banheiro': 'Quantidade de banheiro'}, template='simple_white')

    fig8.update_layout(showlegend=False)
    c2.plotly_chart(fig8, use_container_width=True)

    # =========================================
    # ========== H9 ==========
    # ==========================================
    c3, c4 = st.columns(2)

    c3.subheader('Hipótese 9: Imóveis com mais quartos são em média 20% mais caros')
    c3.write('Falsa. Imóveis com 6-9 quartos são mais caros sendo,149.56% mais caros se comparado a imóveis com 0 a 3 quartos, 48.94% mais caros se comparados a imóveis com 3 a 6 quartos e 107.25% mais caros se comparados a imóveis com 9 a 11 quartos.')
    data['quarto'] = data['bedrooms'].apply(lambda x: '0-3' if (x > 0) & (x < 3) else '3-6' if (x > 3) & (x < 6) else '6-9' if (x > 6) & (x < 9) else '9-11')
    h9 = data[['quarto', 'price']].groupby('quarto').mean().reset_index()
    fig9 = px.bar(h9, x='quarto', y='price', color='quarto', labels={'price': 'Preço', 'quarto': 'Quantidade de quarto'}, template='simple_white')
    fig9.update_layout(showlegend=False)
    c3.plotly_chart(fig9, use_container_width=True)


    return data

def business_recommendations(data):
    # Group the median of properties by region
    dfzip = data[['zipcode', 'price']].groupby('zipcode').median(
    ).reset_index().rename(columns={'price': 'median_price'})

    data = pd.merge(data, dfzip, how='inner', on='zipcode')

    # recommendation list
    data['recomendation'] = data[['price', 'median_price', 'condition']].apply(
        lambda x: 'buy' if (x['price'] < x['median_price']) &
                           (x['condition'] == 5) else 'not buy', axis='columns')

    data['condition'] = data['condition'].map({1: 'too bad',
                                               2: 'bad',
                                               3: 'good',
                                               4: 'very good',
                                               5: 'great'})
    st.header('Purchasing Recommendation Report')

    data = data[data['recomendation'] == 'buy'].copy()
    df3 = data[['id', 'price', 'median_price', 'condition',
                'recomendation']].sort_values('price', ascending=False).reset_index(drop=True)

    st.dataframe(df3)
    st.write(f'{df3.shape[0]} properties are recommended for purchase')

    return data


def sell_repport(data):

    st.header('Sales Recommended Report')
    st.write(''' Conforme o que foi definido, só foram sugeridos imóveis com ótimas condições para compra. 
    Nesse sentido, todos  os imóveis apresentam condições de venda conforme a sazonalidade:  
    30% de margem para Primavera -
    25% de margem para Verão -
    20% de margem para Inverno -
    10% de margem para Outono.
    Levando em consideração apenas o lucro por imóvel,  caso a sugestão de compra e venda seja seguida o lucro total estimado  é de aproximadamente US$ 45 milhões dólares.
''')

    data['date_month'] = pd.to_datetime(data['date']).dt.month
    data['seasonality'] = np.nan

    data['seasonality'] = data['date_month'].apply(
        lambda x: 'winter' if (x == 12 or x <= 2) else
        'spring' if (3 <= x < 6) else
        'summer' if (6 <= x <= 8) else 'Autumn')

    data['sale_price'] = data[['seasonality', 'price']].apply(
        lambda x: x['price'] * 1.30 if x['seasonality'] == 'Spring' else
        x['price'] * 1.25 if x['seasonality'] == 'summer' else
        x['price'] * 1.20 if x['seasonality'] == 'winter' else
        x['price'] * 1.10, axis='columns')

    data['profit'] = data[['sale_price', 'price']].apply(
        lambda x: x['sale_price'] - x['price'], axis='columns')

    st.dataframe(data[['id', 'zipcode', 'seasonality', 'median_price', 'sale_price', 'profit']])


if __name__ =='__main__':
     #ETL
     #data extration
     path = 'kc_house_data.csv'
     url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

     data = get_data( path )
     geofile = get_geofile( url )


     #transformaion
     data = set_feature( data )
     overview_data( data )
     portfolio_density( data, geofile )
     commercial_distribution( data )
     attributes_distribution( data )
     hipoteses(data)
     data = business_recommendations(data)

     # best time for sale
     sell_repport(data)