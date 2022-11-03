#TAD gerador

# -> Operacoes basicas
# -Construtores
def cria_gerador(bits, seed):
    if type(bits) != int or type(seed) != int or (bits != 32 and bits != 64)\
        or seed <= 0 or (bits==32 and seed > 0xFFFFFFFF)\
        or (bits==64 and seed > 0xFFFFFFFFFFFFFFFF):
        raise ValueError('cria_gerador: argumentos invalidos')
    return [bits,seed]

def cria_copia_gerador(gerador):
    if eh_gerador(gerador):
        return gerador.copy()

# -Seletores
def obtem_estado(gerador):
    if eh_gerador(gerador):
        return gerador[1]

# -Modificadores
def define_estado(gerador, seed):
    if eh_gerador(gerador):
        gerador[1] = seed
        return seed

def atualiza_estado(gerador):
    if eh_gerador(gerador):
        valores_da_sequencia = (13, 7, 17) if gerador[0]==64 else (13,17,5)
        bit_a_bit = 0xFFFFFFFFFFFFFFFF if gerador[0]==64 else 0xFFFFFFFF
        gerador[1] ^= (gerador[1] << valores_da_sequencia[0]) & bit_a_bit
        gerador[1] ^= (gerador[1] >> valores_da_sequencia[1]) & bit_a_bit
        gerador[1] ^= (gerador[1] << valores_da_sequencia[2]) & bit_a_bit
        return gerador[1]

# -Reconhenedor
def eh_gerador(arg):
    return type(arg) == list and len(arg) == 2 and type(arg[0]) == int and \
        type(arg[1]) == int and (arg[0] == 32 or arg[0] == 64) and \
            arg[1] > 0

# -Teste
def geradores_iguais(gerador1, gerador2):
    return eh_gerador(gerador1) and eh_gerador(gerador2) and gerador1[0]==gerador2[0]\
        and gerador1[1]==gerador2[1]

# -Transformador
def gerador_para_str(gerador):
    return f'xorshift{gerador[0]}(s={gerador[1]})'

# -> Funcoes de alto nivel
def gera_numero_aleatorio(gerador, n):
    atualiza_estado(gerador)
    return 1 + (obtem_estado(gerador)%n)

def gera_carater_aleatorio(gerador, caracter):
    atualiza_estado(gerador)
    caracteres = [chr(letra) for letra in range(ord('A'), ord(caracter)+1)]
    l = len(caracteres)
    return caracteres[obtem_estado(gerador)%l]

# TAD coordenada 

# -> Operacoes basicas
# -Construtores
def cria_coordenada(coluna, linha):
    if type(coluna) != str or type(linha) != int or len(coluna)!=1 or not(1<=linha<=99) or \
        not('A' <= coluna <= 'Z'):
        raise ValueError('cria_coordenada: argumentos invalidos')

    return (coluna, linha)

# -Seletores
def obtem_coluna(coordenada):
    if eh_coordenada(coordenada):
        return coordenada[0]

def obtem_linha(coordenada):
    if eh_coordenada(coordenada):
        return coordenada[1]

# -Reconhecedor
def eh_coordenada(arg):
    return type(arg) == tuple and len(arg) == 2 and type(arg[0]) == str and \
        type(arg[1]) == int and len(arg[0])== 1 and (1<=arg[1]<=99) and \
        ('A' <= arg[0] <= 'Z')

# Teste
def coordenadas_iguais(coord1, coord2):
    return eh_coordenada(coord1) and eh_coordenada(coord2) and coord1[0]==coord2[0] and \
        coord1[1] == coord2[1]

# -Transformador
def coordenada_para_str(coordenada):
    return f'{coordenada[0]}{str(coordenada[1]).zfill(2)}'

# -> Funcoes de alto nivel
def obtem_coordenadas_vizinhas(coordenada):
    def pode_ser_coordenada(col, lin):
        return type(col) == str and \
            type(lin) == int and len(col)== 1 and (1<=lin<=99) and \
                ('A' <= col <= 'Z')
    coordenadas_vizinhas = []
    # Coordenadas em cima
    for coluna_offset in range(-1, 2):
        linha = obtem_linha(coordenada)-1
        coluna = chr(ord(obtem_coluna(coordenada))+coluna_offset)
        if pode_ser_coordenada(coluna, linha):
            coordenadas_vizinhas.append(cria_coordenada(coluna, linha))
    # Coordenada à direita
    if pode_ser_coordenada(chr(ord(obtem_coluna(coordenada))+1), obtem_linha(coordenada)):
        coordenadas_vizinhas.append(cria_coordenada(chr(ord(obtem_coluna(coordenada))+1), obtem_linha(coordenada)))
    
    # Coordenadas em baixo
    for coluna_offset in range(1, -2, -1):
        linha = obtem_linha(coordenada)+1
        coluna = chr(ord(obtem_coluna(coordenada))+coluna_offset)
        if pode_ser_coordenada(coluna, linha):
            coordenadas_vizinhas.append(cria_coordenada(coluna, linha))
    
    # Coordenada à esquerda
    if pode_ser_coordenada(chr(ord(obtem_coluna(coordenada))-1), obtem_linha(coordenada)):
        coordenadas_vizinhas.append(cria_coordenada(chr(ord(obtem_coluna(coordenada))-1), obtem_linha(coordenada)))

    return tuple(coordenadas_vizinhas)

def obtem_coordenada_aleatoria(coord, gerador):
    coluna = gera_carater_aleatorio(gerador, obtem_coluna(coord))
    linha = gera_numero_aleatorio(gerador, obtem_linha(coord))
    return cria_coordenada(coluna, linha)

# TAD parcela

# -> Operacoes basicas
# -Construtores
def cria_parcela():
    return {'estado':'tapada', 'mina':False}

def cria_copia_parcela(parcela):
    return parcela.copy()

# -Modificadores
def limpa_parcela(parcela):
    if eh_parcela(parcela):
        parcela['estado'] = 'limpa'
        return parcela

def marca_parcela(parcela):
    if eh_parcela(parcela):
        parcela['estado'] = 'marcada'
        return parcela

def desmarca_parcela(parcela):
    if eh_parcela(parcela):
        parcela['estado'] = 'tapada'
        return parcela

def esconde_mina(parcela):
    if eh_parcela(parcela):
        parcela['mina'] = True
        return parcela

# -Reconhecedor
def eh_parcela(arg):
    return type(arg) == dict and len(arg) == 2 and 'estado' in arg \
        and 'mina' in arg and ('limpa' == arg['estado'] \
            or 'marcada' == arg['estado'] or 'tapada' == arg['estado']) \
                and type(arg['mina']) == bool

def eh_parcela_tapada(parcela):
    return eh_parcela(parcela) and parcela['estado'] == 'tapada'

def eh_parcela_marcada(parcela):
    return eh_parcela(parcela) and parcela['estado'] == 'marcada'

def eh_parcela_limpa(parcela):
    return eh_parcela(parcela) and parcela['estado'] == 'limpa'

def eh_parcela_minada(parcela):
    return eh_parcela(parcela) and parcela['mina']

# -Teste
def parcelas_iguais(parcela1, parcela2):
    return eh_parcela(parcela1) and eh_parcela(parcela2) and parcela1['estado'] == parcela2['estado'] \
        and parcela1['mina'] == parcela2['mina']

# -Transformadores
def parcela_para_str(parcela):
    estados = {'tapada': '#', 'marcada': '@', 'limpa_sem_mina': '?', 'limpa_com_mina': 'X'}
    if parcela['estado'] == 'limpa' and parcela['mina']:
        return estados['limpa_com_mina']
    if parcela['estado'] == 'limpa' and not parcela['mina']:
        return estados['limpa_sem_mina']
    return estados[parcela['estado']]

# -> Funcoes de alto nivel
def alterna_bandeira(parcela):
    if eh_parcela(parcela):
        if eh_parcela_marcada(parcela):
            desmarca_parcela(parcela)
            return True
        if eh_parcela_tapada(parcela):
            marca_parcela(parcela)
            return True
    return False

# TAD campo

# -> Operacoes basicas
# -Construtores
def cria_campo(ultima_coluna, ultima_linha):
    if type(ultima_coluna) != str or type(ultima_linha) != int or len(ultima_coluna)!=1\
        or not(1<=ultima_linha<=99) or not(ord('A') <= ord(ultima_coluna) <= ord('Z')):
        raise ValueError('cria_campo: argumentos invalidos')
    numero_colunas = (ord(ultima_coluna)+1)-ord('A')
    return [[cria_parcela() for col in range(numero_colunas)] for lin in range(ultima_linha)]

def cria_copia_campo(campo):
    return list(linha.copy() for linha in campo)

# -Seletores
def obtem_ultima_coluna(campo):
    if eh_campo(campo):
        return chr(ord('A') + (len(campo[0])-1))

def obtem_ultima_linha(campo):
    if eh_campo(campo):
        return len(campo)

def obtem_parcela(campo, coord):
    if eh_coordenada(coord) and eh_campo(campo) and eh_coordenada_do_campo(campo, coord):
        return campo[obtem_linha(coord)-1][ord(obtem_coluna(coord))-ord('A')]

def obtem_coordenadas(campo, estado):
    if eh_campo(campo) and ('limpas' == estado or 'marcadas' == estado\
        or 'tapadas' == estado or 'minadas' == estado):
        if estado == 'limpas':
            filtro = eh_parcela_limpa
        if estado == 'marcadas':
            filtro = eh_parcela_marcada
        if estado == 'tapadas':
            filtro = eh_parcela_tapada
        if estado == 'minadas':
            filtro = eh_parcela_minada
        filtrado = []
        for linha in range(len(campo)):
            for coluna in range(len(campo[0])):
                coluna_letra = chr(ord('A')+coluna)
                if filtro(obtem_parcela(campo, cria_coordenada(coluna_letra, linha+1))):
                    filtrado.append(cria_coordenada(coluna_letra, linha+1))
        return filtrado

def obtem_numero_minas_vizinhas(campo, coord):
    if eh_campo(campo) and eh_coordenada(coord) and eh_coordenada_do_campo(campo, coord):
        coordenadas_vizinhas = obtem_coordenadas_vizinhas(coord)
        num_coordenadas_vizinhas_minadas = 0
        for coordenada in coordenadas_vizinhas:
            index_linha = obtem_linha(coordenada)-1
            index_coluna = ord(obtem_coluna(coordenada))-ord('A')
            if eh_coordenada_do_campo(campo, coordenada) and eh_parcela_minada(campo[index_linha][index_coluna]):
                num_coordenadas_vizinhas_minadas += 1
        return num_coordenadas_vizinhas_minadas

# -Reconhecedores
def eh_campo(arg):
    return type(arg) == list and 1<=len(arg)<=99 \
        and all((type(col)==list and (1<=len(col)<=26)) for col in arg)\
        and all(all(eh_parcela(el) for el in col) for col in arg)

def eh_coordenada_do_campo(campo, coord):
    return eh_campo(campo) and eh_coordenada(coord)\
        and obtem_coluna(coord) <= obtem_ultima_coluna(campo)\
        and obtem_linha(coord) <= obtem_ultima_linha(campo)

# -Teste
def campos_iguais(campo1, campo2):
    return eh_campo(campo1) and eh_campo(campo2) and campo1 == campo2

# -Transformador
def campo_para_str(campo):
    if eh_campo(campo):
        lista_letras = [chr(letra_lista) for letra_lista in range(ord('A'), ord(obtem_ultima_coluna(campo))+1)]
        linhas_do_campo = [f"   {''.join(lista_letras)}", '  +'+'-'*len(lista_letras)+'+']
        for i, linha in enumerate(campo):
            simbolos_linha = [parcela_para_str(parcela) for parcela in linha]
            for j in range(len(linha)):
                if simbolos_linha[j] == '?':
                    coluna_letra = chr(ord('A')+j)
                    numero_minas_vizinhas = obtem_numero_minas_vizinhas(campo, cria_coordenada(coluna_letra, i+1))
                    simbolos_linha[j] = ' ' if numero_minas_vizinhas == 0\
                        else str(numero_minas_vizinhas)
            linhas_do_campo.append(f'{str(i+1).zfill(2)}|{"".join(simbolos_linha)}|')
        linhas_do_campo.append('  +'+'-'*len(lista_letras)+'+')
        return '\n'.join(linhas_do_campo)

# -> Funcoes de alto nivel
def coloca_minas(campo, coordenada, gerador, num_minas):
    for i in range(num_minas):
        while True:
            coordenada_escolhida = obtem_coordenada_aleatoria(cria_coordenada(obtem_ultima_coluna(campo), obtem_ultima_linha(campo)), gerador)   
            coordenadas_vizinhas = obtem_coordenadas_vizinhas(coordenada)
            if not eh_parcela_minada(obtem_parcela(campo, coordenada_escolhida))\
                and not coordenadas_iguais(coordenada, coordenada_escolhida)\
                and coordenada_escolhida not in coordenadas_vizinhas:
                esconde_mina(obtem_parcela(campo, coordenada_escolhida))
                break
    return campo

def limpa_campo(campo, coordenada):
    parcela = obtem_parcela(campo, coordenada)
    if not eh_parcela_limpa(parcela) and not eh_parcela_marcada(parcela):
        limpa_parcela(obtem_parcela(campo, coordenada))
        minas_vizinhas = obtem_numero_minas_vizinhas(campo, coordenada)
        coordenadas_vizinhas = obtem_coordenadas_vizinhas(coordenada)
        if minas_vizinhas == 0:
            for coordenada_vizinha in coordenadas_vizinhas:
                limpa_campo(campo, coordenada_vizinha)

    return campo

# Funcoes adicionais
def jogo_ganho(campo):
    coordenadas_marcadas_ou_tapadas = obtem_coordenadas(campo, 'tapadas') + obtem_coordenadas(campo, 'marcadas')
    coordenadas_marcadas_ou_tapadas.sort(key=lambda coord: (obtem_coluna(coord), obtem_linha(coord)))
    coordenadas_minadas = obtem_coordenadas(campo, 'minadas')
    coordenadas_minadas.sort(key=lambda coord: (obtem_coluna(coord), obtem_linha(coord)))
    return len(coordenadas_marcadas_ou_tapadas) != 0\
        and len(coordenadas_minadas) != 0\
        and coordenadas_marcadas_ou_tapadas == coordenadas_minadas

def turno_jogador(campo, primeiro_turno=False):
    if not primeiro_turno:
        while True:
            acao = input('Escolha uma ação, [L]impar ou [M]arcar:')
            if type(acao)==str and len(acao)==1 and (acao == 'M' or acao == 'L'):
                break
    while True:
        coordenada = input('Escolha uma coordenada:')
        try:
            if type(coordenada) == str and len(coordenada) == 3\
            and 1 <= int(coordenada[1:3]) <= obtem_ultima_linha(campo)\
            and 'A' <= str(coordenada[0]) <= obtem_ultima_coluna(campo):
                coordenada = cria_coordenada(str(coordenada[0]), int(coordenada[1:3]))
                break
        except:
            pass
    
    if not primeiro_turno:
        if acao == 'M':
            marca_parcela(obtem_parcela(campo, coordenada))
            return True
        else:
            limpa_campo(campo, coordenada)
            return not eh_parcela_minada(obtem_parcela(campo, coordenada))
    else:
        return coordenada


def minas(ultima_coluna, ultima_linha, num_minas, dimensao_gerador, seed_inicial):
    if type(ultima_coluna) != str or type(ultima_linha) != int\
    or type(num_minas)!=int or type(dimensao_gerador) != int or type(seed_inicial)!=int\
    or len(ultima_coluna)!=1 or not(1<=ultima_linha<=99)\
    or not ('A' <= ultima_coluna <= 'Z')\
    or num_minas <= 0 or (dimensao_gerador != 32 and dimensao_gerador != 64)\
    or seed_inicial <= 0 or (dimensao_gerador==32 and seed_inicial > 0xFFFFFFFF)\
    or (dimensao_gerador==64 and seed_inicial > 0xFFFFFFFFFFFFFFFF):
        raise ValueError('minas: argumentos invalidos')
    
    dimensao_campo = (ultima_linha-1)*(ord(ultima_coluna)-ord('A')+1)
    if dimensao_campo < (9 + num_minas):
        raise ValueError('minas: argumentos invalidos')
    
    def mostra_campo():
        print(f'   [Bandeiras {len(obtem_coordenadas(campo, "marcadas"))}/{num_minas}]')
        print(campo_para_str(campo))

    campo = cria_campo(ultima_coluna, ultima_linha)
    mostra_campo()
    gerador = cria_gerador(dimensao_gerador, seed_inicial)
    coordenada_inicial = turno_jogador(campo, primeiro_turno=True)
    campo = coloca_minas(campo, coordenada_inicial, gerador, num_minas)
    limpa_campo(campo, coordenada_inicial)

    while True:
        mostra_campo()
        turno = turno_jogador(campo)
        if not turno:
            mostra_campo()
            print('BOOOOOOOM!!!')
            return False
        if jogo_ganho(campo):
            mostra_campo()
            print('VITORIA!!!')
            return True
