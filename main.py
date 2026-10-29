
print("Iniciando análise de segurança...")

servico = "SSH"
print("Serviço:", servico)

usuarios = ["admin", "root", "lucas"]

for usuario in usuarios:
    print("Usuário analisado:", usuario)

tentativas_falhas = 0
falhas_por_usuario = dict()
falhas_por_ip = dict()

try:
    with open("logs.txt", "r", encoding="utf-8") as arquivo:
        for log in arquivo:
            log = log.strip()
            partes = log.split()

           


            if "Failed password" in log:
                if len(partes) < 8:
                    continue

                if partes[4] != "for":
                    continue

                if partes[6] != "from":
                    continue

                tentativas_falhas = tentativas_falhas + 1
                print("Falha encontrada:", log)
                
                usuario = partes[5]
                ip = partes[7]

                if usuario in falhas_por_usuario:
                    falhas_por_usuario[usuario] = falhas_por_usuario[usuario] + 1
                else:
                    falhas_por_usuario[usuario] = 1

                if ip in falhas_por_ip:
                    falhas_por_ip[ip] = falhas_por_ip[ip] + 1
                else:
                    falhas_por_ip[ip] = 1

except FileNotFoundError:
    print("Não foi possível encontrar logs.txt")

else:
    print("\n--- Resumo geral ---")
    print("Total de falhas:", tentativas_falhas)

    print("\n--- Falhas por usuário ---")
    for usuario in falhas_por_usuario:
        print(usuario, ":", falhas_por_usuario[usuario])

    print("\n--- Falhas por IP ---")
    for ip in falhas_por_ip:
        print(ip, ":", falhas_por_ip[ip])

    print("\n--- Alertas gerais ---")
    if tentativas_falhas >= 3:
        print("ALERTA: muitas tentativas de login!")
    else:
        print("Quantidade de falhas dentro do limite definido.")

    print("\n--- Alertas por usuário ---")
    for usuario in falhas_por_usuario:
        if falhas_por_usuario[usuario] >= 3:
            print("ALERTA: usuário atingiu o limite:", usuario)
        else:
            print("Usuário dentro do limite:", usuario)

    print("\n--- Alertas por IP ---")
    for ip in falhas_por_ip:
        if falhas_por_ip[ip] >= 3:
            print("ALERTA: endereço de origem falhou muitas vezes:", ip)
        else:
            print("Endereço de origem dentro do limite:", ip)

    