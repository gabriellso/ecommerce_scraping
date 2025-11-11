# 🛒 E-commerce Scraper

Um projeto simples em **Python + Selenium** para coletar preços e nomes de produtos da Amazon e Mercado Livre, e visualizar os dados com **Streamlit**.

## 🚀 Como usar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Crie um arquivo `urls.csv` com uma coluna:
   ```csv
   url
   https://www.amazon.com.br/dp/XXXXXXXX
   https://www.mercadolivre.com.br/p/XXXXXXXX
   ```

3. Rode o scraper:
   ```bash
   python main.py
   ```

4. Visualize os resultados:
   ```bash
   streamlit run streamlit_app.py
   ```

Os dados serão salvos em `results_produtos.csv`.
