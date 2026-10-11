def campos_do_objeto(objeto):
    campos = []

    for campo in objeto._meta.concrete_fields:
        # Nunca exibir senhas em páginas de detalhes.
        if campo.name.lower() in {"password", "senha"}:
            continue

        valor = getattr(objeto, campo.name)

        if campo.is_relation and valor is not None:
            valor = str(valor)

        campos.append({
            "rotulo": campo.verbose_name.capitalize(),
            "valor": valor if valor not in (None, "") else "—",
        })

    return campos