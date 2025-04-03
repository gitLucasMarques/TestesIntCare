CREATE DATABASE IF NOT EXISTS operadoras_saude;
USE operadoras_saude;

CREATE TABLE IF NOT EXISTS despesas_operadoras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    reg_ans VARCHAR(20) NOT NULL,
    cd_conta_contabil INT NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    vl_saldo_inicial DECIMAL(15, 2) NOT NULL,
    vl_saldo_final DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_data (data),
    INDEX idx_conta_contabil (cd_conta_contabil),
    INDEX idx_operadora (reg_ans)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE '/Users/lucasmarques/Downloads/Testes/Teste 3/csv/1T2023.csv'
INTO TABLE despesas_operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final);
 
LOAD DATA LOCAL INFILE '/Users/lucasmarques/Downloads/Testes/Teste 3/csv/2T2023.csv'
INTO TABLE despesas_operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final);
 
LOAD DATA LOCAL INFILE '/Users/lucasmarques/Downloads/Testes/Teste 3/csv/3T2023.csv'
INTO TABLE despesas_operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final);
 
LOAD DATA LOCAL INFILE '/Users/lucasmarques/Downloads/Testes/Teste 3/csv/4T2023.csv'
INTO TABLE despesas_operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final);
 
LOAD DATA LOCAL INFILE '/Users/lucasmarques/Downloads/Testes/Teste 3/csv/1T2024.csv'
INTO TABLE despesas_operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final);
 
LOAD DATA LOCAL INFILE '/Users/lucasmarques/Downloads/Testes/Teste 3/csv/2T2024.csv'
INTO TABLE despesas_operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final);
 
LOAD DATA LOCAL INFILE '/Users/lucasmarques/Downloads/Testes/Teste 3/csv/3T2024.csv'
INTO TABLE despesas_operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final);
 
LOAD DATA LOCAL INFILE '/Users/lucasmarques/Downloads/Testes/Teste 3/csv/4T2024.csv'
INTO TABLE despesas_operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final);

CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf VARCHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(2),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    regiao_comercializacao VARCHAR(100),
    data_registro_ans DATE,
    INDEX idx_nome_fantasia (nome_fantasia),
    INDEX idx_razao_social (razao_social)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

LOAD DATA LOCAL INFILE '/Users/lucasmarques/Downloads/Testes/Teste 3/csv/Relatorio_cadop.csv'
INTO TABLE operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, 
 complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, 
 representante, cargo_representante, regiao_comercializacao, data_registro_ans);

SELECT DISTINCT cd_conta_contabil, descricao 
FROM despesas_operadoras 
WHERE descricao LIKE '%EVENTOS/%SINISTROS%'
   OR descricao LIKE '%ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
ORDER BY cd_conta_contabil;

WITH ultimo_trimestre AS (
    SELECT DATE_SUB(MAX(data), INTERVAL 3 MONTH) AS data_inicio,
           MAX(data) AS data_fim
    FROM despesas_operadoras
)

SELECT 
    o.nome_fantasia AS Operadora,
    o.registro_ans AS Registro_ANS,
    SUM(d.vl_saldo_final - d.vl_saldo_inicial) AS Total_Despesas,
    CONCAT('R$ ', FORMAT(SUM(d.vl_saldo_final - d.vl_saldo_inicial), 2, 'de_DE')) AS Total_Formatado
FROM 
    despesas_operadoras d
JOIN 
    operadoras o ON d.reg_ans = o.registro_ans
JOIN 
    ultimo_trimestre ut ON d.data BETWEEN ut.data_inicio AND ut.data_fim
WHERE 
    d.cd_conta_contabil IN ('41111', '41121', '41131', '41141', '41151', '41161', '41171', '41181', '41191')
GROUP BY 
    o.nome_fantasia, o.registro_ans
ORDER BY 
    Total_Despesas DESC
LIMIT 10;

WITH ultimo_ano AS (
    SELECT DATE_SUB(MAX(data), INTERVAL 1 YEAR) AS data_inicio,
           MAX(data) AS data_fim
    FROM despesas_operadoras
)

SELECT 
    o.nome_fantasia AS Operadora,
    o.registro_ans AS Registro_ANS,
    SUM(d.vl_saldo_final - d.vl_saldo_inicial) AS Total_Despesas_Anual,
    CONCAT('R$ ', FORMAT(SUM(d.vl_saldo_final - d.vl_saldo_inicial), 2, 'de_DE')) AS Total_Formatado
FROM 
    despesas_operadoras d
JOIN 
    operadoras o ON d.reg_ans = o.registro_ans
JOIN 
    ultimo_ano ua ON d.data BETWEEN ua.data_inicio AND ua.data_fim
WHERE 
    d.cd_conta_contabil IN ('41111', '41121', '41131', '41141', '41151', '41161', '41171', '41181', '41191')
GROUP BY 
    o.nome_fantasia, o.registro_ans
ORDER BY 
    Total_Despesas_Anual DESC
LIMIT 10;