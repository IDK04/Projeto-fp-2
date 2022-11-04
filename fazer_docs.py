funcoes = []
with open('funcoes_original.txt', 'r', encoding='UTF-8') as file:
    for linha in file.readlines():
        linha = linha.split(';')
        entrada = linha[2].split(',')
        saida = linha[3].split(',')
        funcoes.append({'nome':linha[0], 'descricao':linha[1], 'entrada':entrada, 'saida':saida})

with open('funcoes_final.txt', 'w', encoding='UTF-8') as file:
    linhas = []
    for funcao in funcoes:
        linhas.append(f"'''{funcao['descricao']}\n\t{funcao['nome']} : {' x '.join(funcao['entrada'])} -> {' x '.join(funcao['saida'])}\t'''\n\n")
    file.writelines(linhas)