import streamlit as st
import pandas as pd
import sqlite3
from faker import Faker

# Interface Streamlit
def main():
    st.title("ERP Financeiro com Streamlit")
    
    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios", "Fluxo de Caixa por Mês", "Status das Contas a Pagar e Receber", "Top 5 Clientes com Maior Receita"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    
    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)
        
    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)
        
    elif choice == "Relatórios":
        st.subheader("Relatório de Fluxo de Caixa")
        df = pd.read_sql_query("SELECT tipo, SUM(valor) as total FROM lancamentos GROUP BY tipo", conn)
        st.dataframe(df)

    elif choice == "Fluxo de Caixa por Mês":
        st.subheader("Fluxo de Caixa por Mês")
        df = pd.read_sql_query("SELECT strftime('%m-%Y', data) as mes, SUM(valor) as total FROM lancamentos GROUP BY strftime('%m-%Y', data)", conn)
        st.bar_chart(df.set_index("mes"))

    elif choice == "Status das Contas a Pagar e Receber":
        st.subheader("Status das Contas a Pagar e Receber")
        df = pd.read_sql_query("SELECT status, count(*) as total FROM contas_pagar GROUP BY status", conn)
        st.bar_chart(df.set_index("status"))

    elif choice == "Top 5 Clientes com Maior Receita":
        st.subheader("Top 5 Clientes com Maior Receita")
        df = pd.read_sql_query("SELECT clientes.nome as cliente, SUM(contas_receber.valor) as total FROM contas_receber JOIN clientes ON clientes.id = contas_receber.cliente_id GROUP BY clientes.nome ORDER BY total DESC LIMIT 5", conn)
        st.bar_chart(df.set_index("cliente"))

    conn.close()
    
if __name__ == "__main__":
    main()
