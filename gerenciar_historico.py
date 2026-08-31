import google.generativeai as genai


def _extrair_texto(parte):
    if isinstance(parte, str):
        return parte

    if isinstance(parte, dict):
        return parte.get("text", "")

    return getattr(parte, "text", "")


def resumir_historico(historico, modelo_escolhido):
    """Resume o histórico, preservando o contexto essencial da conversa."""
    mensagens = []

    for mensagem in historico:
        if isinstance(mensagem, dict):
            role = mensagem.get("role", "")
            partes = mensagem.get("parts", [])
        else:
            role = getattr(mensagem, "role", "")
            partes = getattr(mensagem, "parts", [])

        texto = " ".join(
            texto
            for parte in partes
            if (texto := _extrair_texto(parte))
        )

        if texto:
            autor = "Usuário" if role == "user" else "Assistente"
            mensagens.append(f"{autor}: {texto}")

    texto_completo = "\n".join(mensagens)

    prompt_resumo = f"""
    Resuma o histórico abaixo mantendo fatos, preferências, dúvidas pendentes e
    informações essenciais para continuar a conversa de forma coerente.
    Não invente informações.

    HISTÓRICO:
    {texto_completo}
    """

    llm = genai.GenerativeModel(
        model_name=modelo_escolhido,
        system_instruction="Você é um assistente especializado em resumir conversas.",
        generation_config={"temperature": 0.1, "max_output_tokens": 512},
    )

    resposta = llm.generate_content(prompt_resumo)
    resumo = resposta.text.strip()

    return [
        {
            "role": "user",
            "parts": ["Recupere o contexto essencial da conversa anterior."],
        },
        {"role": "model", "parts": [resumo]},
    ]
