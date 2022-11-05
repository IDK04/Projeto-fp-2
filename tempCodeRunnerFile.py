m = cria_campo('E',5)
esconde_mina(obtem_parcela(m, cria_coordenada('C', 3)))
limpa_campo(m, cria_coordenada('C', 3))
limpa_campo(m, cria_coordenada('C', 3))
print(campo_para_str(m))

print('   ABCDEFGHIJ\n  +----------+\n01|##########|\n02|##########|\n03|#X#1111111|\n04|###1      |\n05|###1      |\n06|###222211 |\n07|######2X1 |\n08|######211 |\n  +----------+\n')
print('   ABCDEFGHIJ\n  +----------+\n01|##########|\n02|##########|\n03|#X#1111111|\n04|###1      |\n05|###1      |\n06|###222211 |\n07|#######X1 |\n08|########1 |\n  +----------+\n')