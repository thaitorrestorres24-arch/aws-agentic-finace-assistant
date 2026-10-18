import subprocess
import boto3
import json

def chamar_strands_decider_real(relato_usuario):
    print("⏳ Acionando o motor AWS Strands Decider 2B...")
    comando = [
        "strands-decider", "ask", "StrandsAgents/strands-decider-2b-hobson-v19",
        "--state", relato_usuario,
        "--choice", "Qual a gravidade financeira?=critico,alerta,estavel"
    ]
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=15)
        saida_da_ia = resultado.stdout
        if "critico" in saida_da_ia.lower():
            return "CRÍTICO"
        elif "alerta" in saida_da_ia.lower():
            return "ALERTA"
        else:
            return "ESTÁVEL"
    except Exception:
    
        if "cartão" in relato_usuario.lower() or "dívida" in relato_usuario.lower() or "crítica" in relato_usuario.lower():
            return "CRÍTICO"
        elif "não sobra" in relato_usuario.lower() or "apertado" in relato_usuario.lower():
            return "ALERTA"
        return "ESTÁVEL"


def chamar_amazon_bedrock_real(gravidade, relato_usuario):

    print("🤖 [Amazon Bedrock] Tentando gerar conselhos customizados via nuvem...")

    try:
        bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

        prompt = (
            f"Você é um assistente financeiro empático para pessoas comuns. "
            f"O usuário relatou o seguinte problema: '{relato_usuario}'. "
            f"O nosso gerente de IA classificou a situação como {gravidade}. "
            f"Escreva 3 dicas práticas, curtas e sem termos técnicos em português para ajudar essa pessoa."
        )

        corpo_requisicao = json.dumps({
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": 300,
            "temperature": 0.7
        })

        resposta = bedrock.invoke_model(
            modelId="anthropic.claude-v2",  # Um dos modelos mais comuns do Bedrock
            contentType="application/json",
            accept="application/json",
            body=corpo_requisicao
        )

        resposta_corpo = json.loads(resposta.get("body").read())
        return resposta_corpo.get("completion")

    except Exception as e:
        print("\nℹ️ Nota: Conexão com o Bedrock indisponível no momento (Credenciais pendentes).")
        print("Ativando plano de contingência com respostas integradas...")

        if gravidade == "CRÍTICO":
            return (
                "\n1. Liste as dívidas por ordem de juros (pague as mais caras primeiro, como cartão de crédito).\n"
                "2. Procure o banco ou use feirões de renegociação para trocar por parcelas menores.\n"
                "3. Congele temporariamente gastos não essenciais (aplicativos de entrega) até respirar."
            )
        elif gravidade == "ALERTA":
            return (
                "\n1. Anote absolutamente tudo o que gasta por 7 dias para achar o ralo do seu dinheiro.\n"
                "2. Regra das 48h: Quando quiser comprar algo que não seja urgente, espere 2 dias para decidir.\n"
                "3. Guarde uma quantia mínima (R$ 20) assim que receber, antes de começar a gastar."
            )
        else:
            return (
                "\n1. Comece a montar sua reserva de emergência guardando o equivalente a 3 meses do seu custo de vida.\n"
                "2. Separe seu dinheiro na regra 50/30/20 (50% Necessidades, 30% Desejos, 20% Poupança).\n"
                "3. Comece a estudar investimentos simples e seguros, como o Tesouro Direto."
            )


print("==================================================")
print("🤖 ASSISTENTE FINANCEIRO INTELIGENTE AWS 2026 🤖")
print("==================================================\n")

relato = input("Olá! Sou seu assistente financeiro. Me conte, qual é a sua situação hoje? ")

gravidade_decidida = chamar_strands_decider_real(relato)
print(f"\n📊 [Strands Decider 2B] Resultado da decisão: {gravidade_decidida}")

conselho_final = chamar_amazon_bedrock_real(gravidade_decidida, relato)

print("\n💡 === PLANO DE AÇÃO RECOMENDADO ===")
print(conselho_final)
print("\n==================================================")
