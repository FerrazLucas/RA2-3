import json
import sys

# Nome do aluno: Lucas Ferraz

# leitura do arquivo de entrada

def lerArquivo(nomeArquivo):
    with open(nomeArquivo, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo.readlines()]
    return [linha for linha in linhas if linha]



def lerTokens(nomeArquivo):
    linhas = lerArquivo(nomeArquivo)
    return [parseExpressao(linha) for linha in linhas]



# analisador léxico em formato de estados

def parseExpressao(linha):
    tokens = []
    posicao = 0
    lexema = ""

    def guardar(tipo, valor):
        tokens.append((tipo, valor))

    def estado_inicial():
        nonlocal posicao, lexema

        while posicao < len(linha) and linha[posicao].isspace():
            posicao += 1

        if posicao >= len(linha):
            return None

        atual = linha[posicao]

        if atual == "(":
            guardar("LPAREN", "(")
            posicao += 1
            return estado_inicial

        if atual == ")":
            guardar("RPAREN", ")")
            posicao += 1
            return estado_inicial

        if atual == "*":
            guardar("OP", "*")
            posicao += 1
            return estado_inicial

        if atual == "%":
            guardar("OP", "%")
            posicao += 1
            return estado_inicial

        if atual == "^":
            guardar("OP", "^")
            posicao += 1
            return estado_inicial

        if atual == "|":
            guardar("OP", "|")
            posicao += 1
            return estado_inicial

        if atual == "/":
            lexema = "/"
            posicao += 1
            return estado_barra

        if atual in "+-":
            proximo_e_numero = (
                posicao + 1 < len(linha)
                and (linha[posicao + 1].isdigit() or linha[posicao + 1] == ".")
            )

            if proximo_e_numero:
                lexema = atual
                posicao += 1
                return estado_numero

            guardar("OP", atual)
            posicao += 1
            return estado_inicial

        if atual.isdigit() or atual == ".":
            lexema = atual
            posicao += 1
            return estado_numero

        if atual.isalpha() or atual == "_":
            lexema = atual
            posicao += 1
            return estado_identificador

        raise ValueError(f"Caractere inválido: '{atual}'")

    def estado_barra():
        nonlocal posicao, lexema

        if posicao < len(linha) and linha[posicao] == "/":
            posicao += 1

        guardar("OP", "/")
        lexema = ""
        return estado_inicial

    def estado_numero():
        nonlocal posicao, lexema

        achou_ponto = "." in lexema
        achou_digito = any(caractere.isdigit() for caractere in lexema)

        while posicao < len(linha):
            atual = linha[posicao]

            if atual.isdigit():
                lexema += atual
                achou_digito = True
                posicao += 1
                continue

            if atual == "." and not achou_ponto:
                lexema += atual
                achou_ponto = True
                posicao += 1
                continue

            break

        if not achou_digito:
            raise ValueError(f"Número inválido: {lexema}")

        guardar("NUM", lexema)
        lexema = ""
        return estado_inicial

    def estado_identificador():
        nonlocal posicao, lexema

        while posicao < len(linha):
            atual = linha[posicao]
            if atual.isalnum() or atual == "_":
                lexema += atual
                posicao += 1
            else:
                break

        palavras_reservadas = {
            "RES": "RES",
            "START": "START",
            "END": "END",
            "IF": "IF",
            "IFELSE": "IFELSE",
            "WHILE": "WHILE",
        }

        if lexema in palavras_reservadas:
            guardar(palavras_reservadas[lexema], lexema)
        else:
            guardar("ID", lexema)

        lexema = ""
        return estado_inicial

    estado_atual = estado_inicial
    while estado_atual is not None:
        estado_atual = estado_atual()

    return tokens




def _criar_numero(valor):
    return {"tipo": "NUM", "valor": valor}


def _criar_identificador(valor):
    return {"tipo": "ID", "valor": valor}


def _criar_operador(valor):
    return {"tipo": "OP", "valor": valor}


def _criar_reservado_res():
    return {"tipo": "RES"}


def _criar_inicio():
    return {"tipo": "START"}


def _criar_fim():
    return {"tipo": "END"}


def _criar_if():
    return {"tipo": "IF"}


def _criar_if_else():
    return {"tipo": "IFELSE"}


def _criar_while():
    return {"tipo": "WHILE"}


def _criar_binario(operador, esquerdo, direito):
    return {"tipo": "BINOP", "op": operador, "esq": esquerdo, "dir": direito}


def _criar_mem_get(nome):
    return {"tipo": "MEM_GET", "nome": nome}


def _criar_mem_set(nome, expressao):
    return {"tipo": "MEM_SET", "nome": nome, "expr": expressao}


def _criar_ref_res(valor):
    return {"tipo": "RES_REF", "n": valor}


def _criar_no_if(condicao, entao):
    return {"tipo": "IF_CMD", "cond": condicao, "entao": entao}


def _criar_no_if_else(condicao, entao, senao):
    return {"tipo": "IFELSE_CMD", "cond": condicao, "entao": entao, "senao": senao}


def _criar_no_while(condicao, corpo):
    return {"tipo": "WHILE_CMD", "cond": condicao, "corpo": corpo}


def _transformar_token_em_item(token):
    tipo, valor = token

    if tipo == "NUM":
        return _criar_numero(valor)
    if tipo == "ID":
        return _criar_identificador(valor)
    if tipo == "OP":
        return _criar_operador(valor)
    if tipo == "RES":
        return _criar_reservado_res()
    if tipo == "START":
        return _criar_inicio()
    if tipo == "END":
        return _criar_fim()
    if tipo == "IF":
        return _criar_if()
    if tipo == "IFELSE":
        return _criar_if_else()
    if tipo == "WHILE":
        return _criar_while()

    raise ValueError(f"Token inesperado: {token}")



def _fechar_grupo(itens):
    if len(itens) == 1 and itens[0]["tipo"] == "START":
        return _criar_inicio()

    if len(itens) == 1 and itens[0]["tipo"] == "END":
        return _criar_fim()

    if len(itens) == 1 and itens[0]["tipo"] == "ID":
        return _criar_mem_get(itens[0]["valor"])

    if len(itens) == 1:
        return itens[0]

    if len(itens) == 2 and itens[0]["tipo"] == "NUM" and itens[1]["tipo"] == "RES":
        deslocamento = int(float(itens[0]["valor"]))
        if deslocamento <= 0:
            raise ValueError("RES deve usar um número positivo.")
        return _criar_ref_res(deslocamento)

    if len(itens) == 2 and itens[1]["tipo"] == "ID":
        return _criar_mem_set(itens[1]["valor"], itens[0])

    if len(itens) == 3 and itens[2]["tipo"] == "OP":
        return _criar_binario(itens[2]["valor"], itens[0], itens[1])

    if len(itens) == 3 and itens[2]["tipo"] == "IF":
        return _criar_no_if(itens[0], itens[1])

    if len(itens) == 4 and itens[3]["tipo"] == "IFELSE":
        return _criar_no_if_else(itens[0], itens[1], itens[2])

    if len(itens) == 3 and itens[2]["tipo"] == "WHILE":
        return _criar_no_while(itens[0], itens[1])

    raise ValueError("Expressão inválida.")



# parser

def _parsear_tokens(tokens):
    indice = 0

    def ler_item():
        nonlocal indice

        if indice >= len(tokens):
            raise ValueError("Fim inesperado da expressão.")

        tipo, valor = tokens[indice]

        if tipo == "LPAREN":
            return ler_parenteses()

        if tipo in ("NUM", "ID", "OP", "RES", "START", "END", "IF", "IFELSE", "WHILE"):
            indice += 1
            return _transformar_token_em_item((tipo, valor))

        raise ValueError(f"Token inesperado: {(tipo, valor)}")

    def ler_parenteses():
        nonlocal indice

        if indice >= len(tokens) or tokens[indice][0] != "LPAREN":
            raise ValueError("Esperado '('.")

        indice += 1
        conteudo = []

        while True:
            if indice >= len(tokens):
                raise ValueError("Parêntese não fechado.")

            if tokens[indice][0] == "RPAREN":
                indice += 1
                break

            conteudo.append(ler_item())

        return _fechar_grupo(conteudo)

    arvore = ler_item()

    if indice != len(tokens):
        raise ValueError("Tokens sobrando após o fim da expressão.")

    return arvore



def executarExpressao(tokens, historicoResultados, memoria):
    if not tokens:
        raise ValueError("Linha vazia.")

    if tokens[0][0] != "LPAREN" or tokens[-1][0] != "RPAREN":
        raise ValueError("Cada linha deve ser uma expressão entre parênteses.")

    return {
        "tokens": tokens,
        "arvore": _parsear_tokens(tokens),
    }



def construirGramatica():
    return {
        "gramatica": [
            "PROGRAMA -> START BLOCO END",
            "BLOCO -> COMANDO BLOCO | ε",
            "COMANDO -> EXPRESSAO | IF_CMD | IFELSE_CMD | WHILE_CMD",
            "IF_CMD -> ( CONDICAO COMANDO IF )",
            "IFELSE_CMD -> ( CONDICAO COMANDO COMANDO IFELSE )",
            "WHILE_CMD -> ( CONDICAO COMANDO WHILE )",
            "EXPRESSAO -> NUM | ID | ( ID ) | ( NUM RES ) | ( EXPRESSAO ID ) | ( EXPRESSAO EXPRESSAO OP )",
        ],
        "first": {
            "PROGRAMA": ["START"],
            "BLOCO": ["COMANDO", "ε"],
            "COMANDO": ["EXPRESSAO", "IF_CMD", "IFELSE_CMD", "WHILE_CMD"],
            "IF_CMD": ["IF"],
            "IFELSE_CMD": ["IFELSE"],
            "WHILE_CMD": ["WHILE"],
            "EXPRESSAO": ["NUM", "ID", "LPAREN"],
        },
        "follow": {
            "PROGRAMA": ["$"],
            "BLOCO": ["END"],
            "COMANDO": ["COMANDO", "END"],
            "IF_CMD": ["COMANDO", "END"],
            "IFELSE_CMD": ["COMANDO", "END"],
            "WHILE_CMD": ["COMANDO", "END"],
            "EXPRESSAO": ["COMANDO", "END", "IF", "IFELSE", "WHILE", "ID", "OP", "RES", "RPAREN"],
        },
        "tabela": {
            "PROGRAMA": {"START": "START BLOCO END"},
            "BLOCO": {"COMANDO": "COMANDO BLOCO", "END": "ε"},
            "COMANDO": {
                "EXPRESSAO": "EXPRESSAO",
                "IF": "IF_CMD",
                "IFELSE": "IFELSE_CMD",
                "WHILE": "WHILE_CMD",
            },
        },
    }



def parsear(tokensPorLinha, gramatica):
    comandos = []
    historicoResultados = []
    memoria = {}
    inicio_encontrado = False
    fim_encontrado = False
    numero_resultado = 0

    for numero_linha, tokens_linha in enumerate(tokensPorLinha, start=1):
        try:
            estrutura_linha = executarExpressao(tokens_linha, historicoResultados, memoria)
        except Exception as erro:
            raise ValueError(f"Linha {numero_linha}: {erro}")

        no = estrutura_linha["arvore"]

        if numero_linha == 1:
            if no["tipo"] != "START":
                raise ValueError("O programa deve começar com (START).")
            inicio_encontrado = True
            continue

        if no["tipo"] == "START":
            raise ValueError(f"Linha {numero_linha}: (START) só pode aparecer na primeira linha.")

        if no["tipo"] == "END":
            if numero_linha != len(tokensPorLinha):
                raise ValueError(f"Linha {numero_linha}: (END) só pode aparecer na última linha.")
            fim_encontrado = True
            continue

        if fim_encontrado:
            raise ValueError(f"Linha {numero_linha}: comando após (END).")

        numero_resultado += 1
        comandos.append({
            "linha": numero_linha,
            "resultado": numero_resultado,
            "arvore": no,
            "tokens": tokens_linha,
        })
        historicoResultados.append(f"res_{numero_resultado}")

    if not inicio_encontrado:
        raise ValueError("O programa deve começar com (START).")

    if not fim_encontrado:
        raise ValueError("O programa deve terminar com (END).")

    return {
        "tipo": "PROGRAM",
        "gramatica": gramatica,
        "comandos": comandos,
    }



def gerarArvore(programa):
    return programa



def _limpar_nome(nome):
    return "".join(caractere if caractere.isalnum() or caractere == "_" else "_" for caractere in nome)



def _nome_memoria(nome):
    return f"mem_{_limpar_nome(nome)}"



def _juntar_constantes_e_memorias(no, constantes, memorias):
    tipo = no["tipo"]

    if tipo == "NUM":
        if no["valor"] not in constantes:
            constantes[no["valor"]] = f"const_{len(constantes)}"
        return

    if tipo == "ID":
        memorias.add(no["valor"])
        return

    if tipo == "MEM_GET":
        memorias.add(no["nome"])
        return

    if tipo == "MEM_SET":
        memorias.add(no["nome"])
        _juntar_constantes_e_memorias(no["expr"], constantes, memorias)
        return

    if tipo == "BINOP":
        _juntar_constantes_e_memorias(no["esq"], constantes, memorias)
        _juntar_constantes_e_memorias(no["dir"], constantes, memorias)
        return

    if tipo == "IF_CMD":
        _juntar_constantes_e_memorias(no["cond"], constantes, memorias)
        _juntar_constantes_e_memorias(no["entao"], constantes, memorias)
        return

    if tipo == "IFELSE_CMD":
        _juntar_constantes_e_memorias(no["cond"], constantes, memorias)
        _juntar_constantes_e_memorias(no["entao"], constantes, memorias)
        _juntar_constantes_e_memorias(no["senao"], constantes, memorias)
        return

    if tipo == "WHILE_CMD":
        _juntar_constantes_e_memorias(no["cond"], constantes, memorias)
        _juntar_constantes_e_memorias(no["corpo"], constantes, memorias)
        return

    if tipo == "RES_REF":
        return



def _empilhar_d0(codigo):
    codigo.append("    VSTR d0, [r10]")
    codigo.append("    ADD r10, r10, #8")



def _desempilhar_para(codigo, registrador):
    codigo.append("    SUB r10, r10, #8")
    codigo.append(f"    VLDR {registrador}, [r10]")



def _novo_rotulo(contador, prefixo):
    contador["valor"] += 1
    return f"{prefixo}_{contador['valor']}"



def _carregar_zero(codigo, registrador):
    codigo.append("    LDR r0, =const_zero")
    codigo.append(f"    VLDR {registrador}, [r0]")



def _comparar_d0_com_zero(codigo):
    _carregar_zero(codigo, "d1")
    codigo.append("    VCMP.F64 d0, d1")
    codigo.append("    VMRS APSR_nzcv, FPSCR")



def _gerar_no(no, codigo, constantes, linha_atual, contador_rotulos):
    tipo = no["tipo"]

    if tipo == "NUM":
        codigo.append(f"    LDR r0, ={constantes[no['valor']]}")
        codigo.append("    VLDR d0, [r0]")
        return

    if tipo == "ID":
        codigo.append(f"    LDR r0, ={_nome_memoria(no['valor'])}")
        codigo.append("    VLDR d0, [r0]")
        return

    if tipo == "MEM_GET":
        codigo.append(f"    LDR r0, ={_nome_memoria(no['nome'])}")
        codigo.append("    VLDR d0, [r0]")
        return

    if tipo == "RES_REF":
        linha_destino = linha_atual - no["n"]
        if linha_destino <= 0:
            raise ValueError(f"Linha executável {linha_atual}: RES aponta para antes do início do programa.")
        codigo.append(f"    LDR r0, =res_{linha_destino}")
        codigo.append("    VLDR d0, [r0]")
        return

    if tipo == "MEM_SET":
        _gerar_no(no["expr"], codigo, constantes, linha_atual, contador_rotulos)
        codigo.append(f"    LDR r0, ={_nome_memoria(no['nome'])}")
        codigo.append("    VSTR d0, [r0]")
        return

    if tipo == "BINOP":
        _gerar_no(no["esq"], codigo, constantes, linha_atual, contador_rotulos)
        _empilhar_d0(codigo)

        _gerar_no(no["dir"], codigo, constantes, linha_atual, contador_rotulos)
        _empilhar_d0(codigo)

        _desempilhar_para(codigo, "d1")
        _desempilhar_para(codigo, "d0")

        operador = no["op"]

        if operador == "+":
            codigo.append("    VADD.F64 d0, d0, d1")
        elif operador == "-":
            codigo.append("    VSUB.F64 d0, d0, d1")
        elif operador == "*":
            codigo.append("    VMUL.F64 d0, d0, d1")
        elif operador == "|":
            codigo.append("    VDIV.F64 d0, d0, d1")
        elif operador == "/":
            codigo.append("    BL op_div_inteira")
        elif operador == "%":
            codigo.append("    BL op_resto")
        elif operador == "^":
            codigo.append("    BL op_potencia")
        else:
            raise ValueError(f"Operador inválido: {operador}")
        return

    if tipo == "IF_CMD":
        rotulo_fim = _novo_rotulo(contador_rotulos, "fim_if")
        _gerar_no(no["cond"], codigo, constantes, linha_atual, contador_rotulos)
        _comparar_d0_com_zero(codigo)
        codigo.append(f"    BEQ {rotulo_fim}")
        _gerar_no(no["entao"], codigo, constantes, linha_atual, contador_rotulos)
        codigo.append(f"{rotulo_fim}:")
        return

    if tipo == "IFELSE_CMD":
        rotulo_senao = _novo_rotulo(contador_rotulos, "senao")
        rotulo_fim = _novo_rotulo(contador_rotulos, "fim_ifelse")
        _gerar_no(no["cond"], codigo, constantes, linha_atual, contador_rotulos)
        _comparar_d0_com_zero(codigo)
        codigo.append(f"    BEQ {rotulo_senao}")
        _gerar_no(no["entao"], codigo, constantes, linha_atual, contador_rotulos)
        codigo.append(f"    B {rotulo_fim}")
        codigo.append(f"{rotulo_senao}:")
        _gerar_no(no["senao"], codigo, constantes, linha_atual, contador_rotulos)
        codigo.append(f"{rotulo_fim}:")
        return

    if tipo == "WHILE_CMD":
        rotulo_inicio = _novo_rotulo(contador_rotulos, "inicio_while")
        rotulo_fim = _novo_rotulo(contador_rotulos, "fim_while")
        _carregar_zero(codigo, "d0")
        codigo.append(f"{rotulo_inicio}:")
        _gerar_no(no["cond"], codigo, constantes, linha_atual, contador_rotulos)
        _comparar_d0_com_zero(codigo)
        codigo.append(f"    BEQ {rotulo_fim}")
        _gerar_no(no["corpo"], codigo, constantes, linha_atual, contador_rotulos)
        codigo.append(f"    B {rotulo_inicio}")
        codigo.append(f"{rotulo_fim}:")
        return

    raise ValueError(f"Nó inválido: {tipo}")



# geração do assembly

def gerarAssembly(arvore):
    constantes = {"0.0": "const_zero", "1.0": "const_um"}
    memorias = set()

    for comando in arvore["comandos"]:
        _juntar_constantes_e_memorias(comando["arvore"], constantes, memorias)

    codigo = []
    codigo.append(".data")
    codigo.append("")
    codigo.append("const_zero: .double 0.0")
    codigo.append("const_um: .double 1.0")

    for valor, rotulo in constantes.items():
        if valor in ("0.0", "1.0"):
            continue
        codigo.append(f"{rotulo}: .double {valor}")

    codigo.append("")
    for nome in sorted(memorias):
        codigo.append(f"{_nome_memoria(nome)}: .double 0.0")

    codigo.append("")
    for numero_linha in range(1, len(arvore["comandos"]) + 1):
        codigo.append(f"res_{numero_linha}: .double 0.0")

    codigo.append("")
    codigo.append("pilha: .space 8192")
    codigo.append("")
    codigo.append(".text")
    codigo.append(".global _start")
    codigo.append("")
    codigo.append("_start:")
    codigo.append("    LDR r10, =pilha")
    codigo.append("")

    contador_rotulos = {"valor": 0}

    for comando in arvore["comandos"]:
        _gerar_no(comando["arvore"], codigo, constantes, comando["resultado"], contador_rotulos)
        codigo.append(f"    LDR r0, =res_{comando['resultado']}")
        codigo.append("    VSTR d0, [r0]")
        codigo.append("")

    codigo.append("fim:")
    codigo.append("    B fim")
    codigo.append("")

    codigo.extend([
        "op_div_inteira:",
        "    VCVT.S32.F64 s0, d0",
        "    VMOV r0, s0",
        "    VCVT.S32.F64 s1, d1",
        "    VMOV r1, s1",
        "    CMP r1, #0",
        "    BEQ op_div_zero",
        "    MOV r2, #0",
        "    MOV r3, #0",
        "    CMP r0, #0",
        "    BGE op_div_a_ok",
        "    RSB r0, r0, #0",
        "    EOR r3, r3, #1",
        "op_div_a_ok:",
        "    CMP r1, #0",
        "    BGE op_div_b_ok",
        "    RSB r1, r1, #0",
        "    EOR r3, r3, #1",
        "op_div_b_ok:",
        "op_div_loop:",
        "    CMP r0, r1",
        "    BLT op_div_fim_loop",
        "    SUB r0, r0, r1",
        "    ADD r2, r2, #1",
        "    B op_div_loop",
        "op_div_fim_loop:",
        "    CMP r3, #0",
        "    BEQ op_div_sinal_ok",
        "    RSB r2, r2, #0",
        "op_div_sinal_ok:",
        "    VMOV s0, r2",
        "    VCVT.F64.S32 d0, s0",
        "    BX lr",
        "",
        "op_resto:",
        "    VCVT.S32.F64 s0, d0",
        "    VMOV r0, s0",
        "    VCVT.S32.F64 s1, d1",
        "    VMOV r1, s1",
        "    CMP r1, #0",
        "    BEQ op_div_zero",
        "    MOV r3, #0",
        "    CMP r0, #0",
        "    BGE op_rest_a_ok",
        "    RSB r0, r0, #0",
        "    MOV r3, #1",
        "op_rest_a_ok:",
        "    CMP r1, #0",
        "    BGE op_rest_b_ok",
        "    RSB r1, r1, #0",
        "op_rest_b_ok:",
        "op_rest_loop:",
        "    CMP r0, r1",
        "    BLT op_rest_fim_loop",
        "    SUB r0, r0, r1",
        "    B op_rest_loop",
        "op_rest_fim_loop:",
        "    CMP r3, #0",
        "    BEQ op_rest_sinal_ok",
        "    RSB r0, r0, #0",
        "op_rest_sinal_ok:",
        "    VMOV s0, r0",
        "    VCVT.F64.S32 d0, s0",
        "    BX lr",
        "",
        "op_potencia:",
        "    VMOV.F64 d2, d0",
        "    VCVT.S32.F64 s1, d1",
        "    VMOV r1, s1",
        "    LDR r0, =const_um",
        "    VLDR d0, [r0]",
        "    CMP r1, #0",
        "    BEQ op_pot_fim",
        "    MOV r2, #0",
        "    CMP r1, #0",
        "    BGE op_pot_exp_ok",
        "    RSB r1, r1, #0",
        "    MOV r2, #1",
        "op_pot_exp_ok:",
        "op_pot_loop:",
        "    CMP r1, #0",
        "    BEQ op_pot_loop_fim",
        "    VMUL.F64 d0, d0, d2",
        "    SUB r1, r1, #1",
        "    B op_pot_loop",
        "op_pot_loop_fim:",
        "    CMP r2, #0",
        "    BEQ op_pot_fim",
        "    LDR r0, =const_um",
        "    VLDR d1, [r0]",
        "    VDIV.F64 d0, d1, d0",
        "op_pot_fim:",
        "    BX lr",
        "",
        "op_div_zero:",
        "    LDR r0, =const_zero",
        "    VLDR d0, [r0]",
        "    BX lr",
    ])

    return "\n".join(codigo)



def _formatar_gramatica(gramatica):
    linhas = []

    linhas.append("GRAMATICA")
    linhas.append("")
    for producao in gramatica["gramatica"]:
        linhas.append(producao)

    linhas.append("")
    linhas.append("FIRST")
    linhas.append("")
    for simbolo, itens in gramatica["first"].items():
        linhas.append(f"FIRST({simbolo}) = {{ {', '.join(itens)} }}")

    linhas.append("")
    linhas.append("FOLLOW")
    linhas.append("")
    for simbolo, itens in gramatica["follow"].items():
        linhas.append(f"FOLLOW({simbolo}) = {{ {', '.join(itens)} }}")

    linhas.append("")
    linhas.append("TABELA LL(1)")
    linhas.append("")
    for nao_terminal, regras in gramatica["tabela"].items():
        for terminal, producao in regras.items():
            linhas.append(f"M[{nao_terminal}, {terminal}] = {producao}")

    return "\n".join(linhas)



# saída

def exibirResultados(tokensPorLinha, arvore, assemblyFinal):
    with open("tokens_saida.txt", "w", encoding="utf-8") as arquivo_tokens:
        for numero_linha, lista_tokens in enumerate(tokensPorLinha, start=1):
            arquivo_tokens.write(f"Linha {numero_linha}:\n")
            for tipo, valor in lista_tokens:
                arquivo_tokens.write(f"  ({tipo}, {valor})\n")
            arquivo_tokens.write("\n")

    with open("arvore_saida.json", "w", encoding="utf-8") as arquivo_arvore:
        json.dump(arvore, arquivo_arvore, ensure_ascii=False, indent=2)

    with open("saida.s", "w", encoding="utf-8") as arquivo_assembly:
        arquivo_assembly.write(assemblyFinal)

    with open("analise_sintatica.txt", "w", encoding="utf-8") as arquivo_gramatica:
        arquivo_gramatica.write(_formatar_gramatica(arvore["gramatica"]))

    print("Arquivos gerados com sucesso:")
    print("- tokens_saida.txt")
    print("- arvore_saida.json")
    print("- analise_sintatica.txt")
    print("- saida.s")



# main

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py arquivo.txt")
        return

    nomeArquivo = sys.argv[1]

    try:
        tokensPorLinha = lerTokens(nomeArquivo)
        gramatica = construirGramatica()
        programa = parsear(tokensPorLinha, gramatica)
        arvore = gerarArvore(programa)
        assemblyFinal = gerarAssembly(arvore)
        exibirResultados(tokensPorLinha, arvore, assemblyFinal)

    except Exception as erro:
        print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
