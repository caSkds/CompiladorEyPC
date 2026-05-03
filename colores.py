def generateHTML(outputPath=None):
    global instructionList, START_ADDRESS, subroutines

    try:
        currentAddress = int(START_ADDRESS, 16)
    except:
        currentAddress = 0x8000

    lines_out = []

    for (etiqueta, opcode, operandos_hex, fuente) in instructionList:

        if opcode is None:
            lines_out.append(f"<div style='margin-left:200px'>{etiqueta}</div>")
            continue

        # ===== OPCODE =====
        opcode_bytes = []
        if isinstance(opcode, str):
            opcode_bytes = [opcode[i:i+2] for i in range(0, len(opcode), 2)]
        else:
            opcode_bytes = [format(opcode, '02X')]

        # ===== OPERANDOS =====
        operandos_resueltos = []
        for op in operandos_hex:
            if any(s.name == op for s in subroutines):
                operandos_resueltos.append("??")
            else:
                operandos_resueltos.append(op.upper() if op else "??")

        operando_bytes = []
        for op in operandos_resueltos:
            for i in range(0, len(op), 2):
                byte = op[i:i+2]
                if len(byte) == 1:
                    byte = "0" + byte
                operando_bytes.append(byte)

        # ===== COLORES =====
        opcode_html = " ".join([f"<span style='color:red'>{b}</span>" for b in opcode_bytes])
        operand_html = " ".join([f"<span style='color:blue'>{b}</span>" for b in operando_bytes])

        addr_str = format(currentAddress & 0xFFFF, '04X')

        linea = f"""
        <div>
            <span style='color:black'>{addr_str}</span>
            {opcode_html} {operand_html}
            <span style='margin-left:20px'>{fuente}</span>
        </div>
        """

        lines_out.append(linea)

        currentAddress += len(opcode_bytes) + len(operando_bytes)

    html = f"""
    <html>
    <body style='font-family: monospace'>
    {''.join(lines_out)}
    </body>
    </html>
    """

    if outputPath:
        with open(outputPath, "w") as f:
            f.write(html)

    return html