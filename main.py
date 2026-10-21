import flet as ft

# --- Funciones auxiliares ---
def validar_nombre(nombre: str) -> bool:
    """Verifica que el nombre no esté vacío y contenga solo letras y espacios."""
    return nombre and all(c.isalpha() or c.isspace() for c in nombre)

def calcular_precio(procesador, ram, gpu, ssd, armado, entrega):
    """Suma los costos de los componentes seleccionados."""
    subtotal = 0
    consumo = 150  # margen base del sistema

    # Procesador
    if procesador == "Intel i5":
        subtotal += 390000; consumo += 65
    elif procesador == "Intel i7":
        subtotal += 1400000; consumo += 65
    elif procesador == "AMD Ryzen 5":
        subtotal += 330000; consumo += 65
    elif procesador == "AMD Ryzen 7":
        subtotal += 950000; consumo += 65

    # RAM (cada 8GB = $100000)
    subtotal += (ram // 8) * 100000

    # Adicionales
    if gpu: subtotal += 500000; consumo += 115
    if ssd: subtotal += 150000
    if armado: subtotal += 30000
    if entrega: subtotal += 10000

    return subtotal, consumo

def aplicar_pago(subtotal, pago):
    """Aplica descuento o recargo según medio de pago."""
    if pago == "efectivo":
        return subtotal * 0.9, None
    elif pago == "debito":
        return subtotal, None
    elif pago == "credito":
        total = subtotal * 1.15
        return total, total / 3

def recomendar_fuente(consumo_total):
    """Sugiere fuente de poder según consumo eléctrico."""
    if consumo_total > 450:
        return "Recomendación: Fuente de 650W o superior."
    else:
        return "Recomendación: Fuente de 500W."

# --- Función principal ---
def main(page: ft.Page):
    page.title = "Cotizador - La Caverna del Nerd"

    # --- Declaración de componentes ---
    nombre = ft.TextField(label="Nombre del cliente")
    presupuesto = ft.TextField(label="Presupuesto disponible (en $)")
    resultado = ft.Text("")

    procesador = ft.Dropdown(
        label="Procesador",
        options=[
            ft.dropdown.Option("Intel i5"),
            ft.dropdown.Option("Intel i7"),
            ft.dropdown.Option("AMD Ryzen 5"),
            ft.dropdown.Option("AMD Ryzen 7"),
        ]
    )

    # Slider + texto dinámico para mostrar valor
    ram_valor = ft.Text("RAM seleccionada: 8 GB")
    ram = ft.Slider(label="Memoria RAM (GB)", min=8, max=64, divisions=7, value=8)

    def actualizar_ram(e):
        ram_valor.value = f"RAM seleccionada: {int(ram.value)} GB"
        page.update()

    ram.on_change = actualizar_ram

    gpu = ft.Checkbox(label="Placa de video dedicada (+$500000, 150W)")
    ssd = ft.Checkbox(label="Unidad SSD extra (+$150000)")
    armado = ft.Checkbox(label="Servicio de armado (+$30000)")
    entrega = ft.Switch(label="Envío a domicilio (+$10000)")

    pago = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="efectivo", label="Efectivo / Transferencia (-10%)"),
            ft.Radio(value="debito", label="Tarjeta Débito (precio lista)"),
            ft.Radio(value="credito", label="Tarjeta Crédito 3 cuotas (+15%)"),
        ])
    )

    # --- Controlador de evento ---
    def calcular(e):
        try:
            # Validaciones
            if not validar_nombre(nombre.value):
                resultado.value = "Error: el nombre debe contener solo letras."
                page.update(); return

            presupuesto_cliente = float(presupuesto.value)
            if not procesador.value or not pago.value:
                resultado.value = "Error: debes elegir procesador y forma de pago."
                page.update(); return

            # Cálculos
            subtotal, consumo = calcular_precio(
                procesador.value, ram.value,
                gpu.value, ssd.value, armado.value, entrega.value
            )
            total, cuotas = aplicar_pago(subtotal, pago.value)
            consumo_total = consumo * 1.25
            fuente = recomendar_fuente(consumo_total)

            # Comparación con presupuesto
            if total <= presupuesto_cliente:
                mensaje = f"Aprobado ✅. Total: ${total:.2f}"
                if cuotas: mensaje += f" | 3 cuotas de ${cuotas:.2f}"
            else:
                faltante = total - presupuesto_cliente
                mensaje = f"Presupuesto insuficiente ❌. Faltan ${faltante:.2f}"

            resultado.value = f"{mensaje}\n{fuente}"
            page.update()

        except ValueError:
            resultado.value = "Error: ingresa valores numéricos válidos en presupuesto."
            page.update()

    # --- Botón de acción ---
    boton = ft.Button("Calcular Cotización", on_click=calcular)
    page.on_submit = calcular
    # --- Ensamblado final ---
    page.add(
        nombre, presupuesto,
        procesador, ram, ram_valor,
        gpu, ssd, armado, entrega,
        pago,
        boton, resultado
    )

ft.run(main)
