from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from fuzzywuzzy import fuzz

app = Flask(__name__)
CORS(app)

df = pd.read_csv('Relatorio_cadop.csv', sep=';', encoding='utf-8')

@app.route('/api/search', methods=['GET'])
def search_operadoras():
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 2:
        return jsonify([])
    
    def calculate_score(row):
        scores = []
        query_lower = query.lower()
        
        if pd.notna(row['Registro_ANS']):
            reg_ans = str(row['Registro_ANS']).strip()
            if query == reg_ans:
                return 100
            
            if query in reg_ans:
                scores.append(90 + fuzz.ratio(query, reg_ans)/10)
    
        if pd.notna(row['Razao_Social']):
            razao_social = str(row['Razao_Social']).lower()
            if query_lower in razao_social:
                scores.append(85)
            scores.append(fuzz.token_set_ratio(query_lower, razao_social))
        
        if pd.notna(row['Nome_Fantasia']):
            nome_fantasia = str(row['Nome_Fantasia']).lower()
            if query_lower in nome_fantasia:
                scores.append(80)
            scores.append(fuzz.token_set_ratio(query_lower, nome_fantasia))
        
        return max(scores) if scores else 0
    
    df['score'] = df.apply(calculate_score, axis=1)

    results = df[df['score'] > 40].sort_values('score', ascending=False)
    
    output = results[[
        'Registro_ANS', 
        'Razao_Social', 
        'Nome_Fantasia', 
        'CNPJ', 
        'Modalidade',
        'score'
    ]].to_dict(orient='records')
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True, port=5000)