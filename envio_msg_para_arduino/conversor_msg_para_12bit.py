import re


"""CONSTANTES"""
DAC_min = 1064 #equivale a 1.3V
DAC_0 = 1884 #equivale a 2.3V
DAC_max = 2664 #equivale a 3.3V
max_variacao_pos = DAC_max - DAC_0 #intervalo maximo de variacao positiva 2.3V a 3.3V
max_variacao_neg = DAC_0 - DAC_min #intervalo maximo de variacao negativa 2.3V a 1.3V

"""MENSAGEM RECEBIDA VIA SOCKET"""
msg_recebida='X=-30%,Y=-50%'

"""TRATAMENTO DA MENSAGEM RECEBIDA"""
vetor_mensagem = msg_recebida.split(",",1)

sinal_X = '-' in vetor_mensagem[0]
sinal_Y = '-' in vetor_mensagem[1]

vetor_valores = re.findall('\d+', msg_recebida)

X = float(vetor_valores[0])
Y = float(vetor_valores[1])

if sinal_X==True: # caso X seja negativo
    X = X*(-1)

if sinal_Y==True: # caso Y seja negativo
    Y= Y*(-1)


"""CONVERSAO DO DAC_X PARA 12BIT"""
if X > 0:
    porcentX = X/100
    dacX = DAC_0 + round(porcentX*max_variacao_pos)

if X == 0:
    dacX = DAC_0

if X < 0:
    porcentX = abs(X/100) #modulo do numero dividido por 100
    dacX = DAC_0 - round(porcentX*max_variacao_neg)


"""CONVERSAO DO DAC_Y PARA 12BIT"""
if  Y > 0:
    porcentY = Y/100
    dacY = DAC_0 + round(porcentY*max_variacao_pos)

if Y == 0:
    dacY = DAC_0

if Y < 0:
    porcentY = abs(Y/100) #modulo do numero dividido por 100
    dacY = DAC_0 - round(porcentY*max_variacao_neg)


print dacX

print dacY
