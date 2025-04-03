#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import zipfile
import pandas as pd
import tabula
import csv

def instalar_dependencias():
    requeridas = {'pandas': 'pandas', 'tabula-py': 'tabula', 'jpype': 'jpype1'}
    print("Verificando dependências...")
    for lib, pkg in requeridas.items():
        try:
            __import__(pkg)
            print(f"✓ {lib} já instalado")
        except ImportError:
            print(f"Instalando {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

def extrair_pdf_para_dataframe(pdf_path):
    print(f"\nExtraindo dados de {pdf_path}...")
    try:
        dfs = tabula.read_pdf(
            pdf_path,
            pages='all',
            multiple_tables=True,
            lattice=True,
            pandas_options={'header': None},
            encoding='latin1'
        )

        if not dfs:
            print("Nenhuma tabela encontrada no PDF.")
            return pd.DataFrame()

        dados_combinados = []
        for df in dfs:
            df = df.dropna(how='all')
            df = df.applymap(lambda x: ' '.join(str(x).splitlines()) if pd.notna(x) else x)
            dados_combinados.append(df)

        final_df = pd.concat(dados_combinados, ignore_index=True)
        
        if not final_df.empty and len(final_df) > 1:
            final_df.columns = final_df.iloc[0]
            final_df = final_df.iloc[1:]
        
        print(f"Total de linhas extraídas: {len(final_df)}")
        return final_df

    except Exception as e:
        print(f"Erro na extração: {str(e)}")
        return pd.DataFrame()

def processar_colunas(df):
    colunas_processar = ['OD', 'AMB', 'HCO', 'HSO', 'REF', 'PAC', 'DUT']

    for col in df.columns:
        if col in colunas_processar:
            df[col] = df[col].astype(str).str.strip().str.upper()

    return df

def tratar_csv_final(df):
    if 'OD' in df.columns:
        df['OD'] = df['OD'].replace({'OD': 'Seg. Odontológica'})
    
    if 'AMB' in df.columns:
        df['AMB'] = df['AMB'].replace({'AMB': 'Seg. Ambulatorial'})
    
    return df

def salvar_para_zip(df, csv_nome, zip_nome):
    if not csv_nome.endswith('.csv'):
        csv_nome += '.csv'

    df = tratar_csv_final(df)
    df = df.fillna('')
    
    with open(csv_nome, 'w', encoding='utf-8-sig', newline='') as f:
        df.to_csv(
            f,
            index=False,
            quoting=csv.QUOTE_MINIMAL,
            escapechar='\\'
        )
    
    with zipfile.ZipFile(zip_nome, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(csv_nome)
    
    os.remove(csv_nome)
    print(f"\nArquivos criados com sucesso: {zip_nome}")

def main():
    instalar_dependencias()
    
    pdf_path = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    csv_nome = "Rol_Procedimentos.csv"
    zip_nome = "Teste_Lucas_Alves_Nascimento_Marques.zip"
    
    if not os.path.exists(pdf_path):
        print(f"\nErro: Arquivo {pdf_path} não encontrado!")
        return
    
    df = extrair_pdf_para_dataframe(pdf_path)
    if df.empty:
        return
    
    df = processar_colunas(df)
    salvar_para_zip(df, csv_nome, zip_nome)
    print("\nProcesso concluído com sucesso!")

if __name__ == "__main__":
    main()