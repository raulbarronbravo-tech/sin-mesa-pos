import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE LA PÁGINA Y MARCA
st.set_page_config(page_title="SIN MESA - POS", layout="wide", initial_sidebar_state="collapsed")

# Estilos visuales con tus colores institucionales (Verde Quimera y Naranja Zumo)
st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7; } 
    h1, h2, h3 { color: #155E3B !important; font-family: 'Arial Black', sans-serif; } 
    
    /* Estilo para los botones de tamaño (Verde Quimera) */
    .stButton>button {
        background-color: #155E3B; color: white; border-radius: 8px; font-weight: bold;
        padding: 8px 12px; width: 100%; border: none; transition: 0.2s; font-size: 13px;
    }
    .stButton>button:hover { background-color: #E26D27; color: white; } 
    
    /* Estilo especial para el botón gigante de cobrar (Naranja Zumo) */
    .boton-cobrar>div>button { 
        background-color: #E26D27 !important; color: white !important; 
        font-size: 20px !important; padding: 18px !important; border-radius: 12px !important;
    }
    
    /* Tarjetas de métricas en el administrador */
    .card-metrica {
        background-color: white; border: 2px solid #155E3B; border-radius: 15px;
        padding: 20px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Filas del menú ordenadas */
    .fila-menu {
        padding: 8px 0px;
        border-bottom: 1px solid #EAE6DF;
        display: flex;
        align-items: center;
    }
    
    .personaje-flotante {
        position: fixed; bottom: 20px; left: 20px; z-index: 99; pointer-events: none;
    }
    </style>
""", unsafe_allow_html=True)

# 2. BASE DE DATOS ESTRUCTURADA POR PRODUCTO Y TAMAÑOS (Tu menú real)
if 'menu_estructurado' not in st.session_state:
    st.session_state.menu_estructurado = {
        "Café Clásico": [
            {"nombre": "Expreso Sencillo", "precios": {"Único": 26.0}},
            {"nombre": "Expreso Doble", "precios": {"Único": 36.0}},
            {"nombre": "Expreso Macchiato", "precios": {"Único": 38.0}},
            {"nombre": "Expreso Tonic", "precios": {"Frío 16oz": 46.0}},
            {"nombre": "Capuchino Regular", "precios": {"8oz": 45.0, "12oz": 55.0, "Frío 16oz": 65.0}},
            {"nombre": "Latte", "precios": {"8oz": 45.0, "12oz": 55.0, "Frío 16oz": 65.0}},
            {"nombre": "Moka", "precios": {"8oz": 45.0, "12oz": 55.0, "Frío 16oz": 65.0}},
            {"nombre": "Flat White", "precios": {"8oz": 45.0, "12oz": 55.0}},
            {"nombre": "Americano", "precios": {"8oz": 40.0, "12oz": 50.0, "Frío 16oz": 65.0}},
        ],
        "Cold Brew": [
            {"nombre": "Cold Brew Tonic", "precios": {"16oz": 69.0}},
            {"nombre": "Cold Brew Mineral", "precios": {"16oz": 69.0}},
            {"nombre": "Cold Brew Guayaba", "precios": {"16oz": 69.0}},
            {"nombre": "Cold Brew Mango", "precios": {"16oz": 69.0}},
        ],
        "Café con Sabor": [
            {"nombre": "Capuchino Menta", "precios": {"8oz": 50.0, "12oz": 60.0, "Frío 16oz": 69.0}},
            {"nombre": "Capuchino Vainilla", "precios": {"8oz": 50.0, "12oz": 60.0, "Frío 16oz": 69.0}},
            {"nombre": "Capuchino Caramelo", "precios": {"8oz": 50.0, "12oz": 60.0, "Frío 16oz": 69.0}},
            {"nombre": "Capuchino Crema Irlandesa", "precios": {"8oz": 50.0, "12oz": 60.0, "Frío 16oz": 69.0}},
        ],
        "Batidos": [
            {"nombre": "Batido Proteína Fresa", "precios": {"16oz": 64.0}},
            {"nombre": "Batido Proteína Plátano", "precios": {"16oz": 64.0}},
            {"nombre": "Batido Proteína Fresa + Plátano", "precios": {"16oz": 75.0}},
        ],
        "Panadería": [
            # Espacios obligatorios listos para que los edites después
            {"nombre": "Pan Dulce 1 (Por definir)", "precios": {"Pieza": 30.0}},
            {"nombre": "Pan Dulce 2 (Por definir)", "precios": {"Pieza": 30.0}},
            {"nombre": "Pan Dulce 3 (Por definir)", "precios": {"Pieza": 35.0}},
            {"nombre": "Pan Dulce 4 (Por definir)", "precios": {"Pieza": 35.0}},
            {"nombre": "Pan Dulce 5 (Por definir)", "precios": {"Pieza": 40.0}},
            {"nombre": "Pan Salado 1 (Por definir)", "precios": {"Pieza": 45.0}},
        ]
    }

if 'carrito' not in st.session_state: st.session_state.carrito = {}
if 'historial_ventas' not in st.session_state: st.session_state.historial_ventas = []

# 3. ENCABEZADO SUPERIOR
col_logo, col_nav = st.columns([2, 1])
with col_logo:
    st.title("☕ SIN MESA")
    st.subheader("Café, Pan y Batidos de Proteína")
with col_nav:
    modo = st.radio("Panel de Control:", ["Ventas (Barra)", "Administrador"], horizontal=True)

st.write("---")

# 4. SISTEMA DE VENTAS TÁCTIL (ESTILO MENÚ LISTA)
if modo == "Ventas (Barra)":
    col_izq, col_der = st.columns([5, 3])
    
    with col_izq:
        st.write("### 📋 Menú Digital")
        
        # Filtro por grandes categorías
        cat_seleccionada = st.selectbox("Filtrar categoría:", list(st.session_state.menu_estructurado.keys()))
        st.write("")
        
        # Mostrar los productos de la categoría seleccionada como una lista limpia
        lista_productos = st.session_state.menu_estructurado[cat_seleccionada]
        
        for idx, prod in enumerate(lista_productos):
            # Creamos una fila visual: Nombre a la izquierda, botones de tamaños a la derecha
            col_nombre, col_t1, col_t2, col_t3 = st.columns([4, 2, 2, 2])
            
            with col_nombre:
                st.markdown(f"<div style='padding-top: 8px;'><b>{prod['nombre']}</b></div>", unsafe_allow_html=True)
            
            # Mapeo y dibujo de botones dinámicos según los tamaños que tenga el producto
            tamanios = list(prod['precios'].keys())
            precios = prod['precios']
            
            # Botón 1
            with col_t1:
                if len(tamanios) > 0:
                    t_nombre = tamanios[0]
                    t_precio = precios[t_nombre]
                    label = f"{t_nombre}\n${t_precio:.0f}" if t_nombre != "Único" and t_nombre != "Pieza" else f"${t_precio:.0f}"
                    if st.button(label, key=f"btn_{cat_seleccionada}_{idx}_{t_nombre}"):
                        item_id = f"{prod['nombre']}_{t_nombre}"
                        if item_id in st.session_state.carrito:
                            st.session_state.carrito[item_id]['cantidad'] += 1
                        else:
                            st.session_state.carrito[item_id] = {'nombre': f"{prod['nombre']} ({t_nombre})" if t_nombre not in ["Único", "Pieza"] else prod['nombre'], 'precio': t_precio, 'cantidad': 1}
                        st.rerun()
            
            # Botón 2
            with col_t2:
                if len(tamanios) > 1:
                    t_nombre = tamanios[1]
                    t_precio = precios[t_nombre]
                    if st.button(f"{t_nombre}\n${t_precio:.0f}", key=f"btn_{cat_seleccionada}_{idx}_{t_nombre}"):
                        item_id = f"{prod['nombre']}_{t_nombre}"
                        if item_id in st.session_state.carrito:
                            st.session_state.carrito[item_id]['cantidad'] += 1
                        else:
                            st.session_state.carrito[item_id] = {'nombre': f"{prod['nombre']} ({t_nombre})", 'precio': t_precio, 'cantidad': 1}
                        st.rerun()
            
            # Botón 3
            with col_t3:
                if len(tamanios) > 2:
                    t_nombre = tamanios[2]
                    t_precio = precios[t_nombre]
                    if st.button(f"{t_nombre}\n${t_precio:.0f}", key=f"btn_{cat_seleccionada}_{idx}_{t_nombre}"):
                        item_id = f"{prod['nombre']}_{t_nombre}"
                        if item_id in st.session_state.carrito:
                            st.session_state.carrito[item_id]['cantidad'] += 1
                        else:
                            st.session_state.carrito[item_id] = {'nombre': f"{prod['nombre']} ({t_nombre})", 'precio': t_precio, 'cantidad': 1}
                        st.rerun()
            st.markdown("<hr style='margin: 4px 0px; border-color: #F1EDE7;'>", unsafe_allow_html=True)

        # Espacio reservado para tu taza animada
        if os.path.exists("personaje.png"):
            st.markdown('<div class="personaje-flotante">', unsafe_allow_html=True)
            st.image("personaje.png", width=110)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        st.write("### 🛒 Orden Actual")
        if not st.session_state.carrito:
            st.info("Toca un precio a la izquierda para agregar a la orden.")
        else:
            total_orden = 0.0
            items_a_eliminar = []
            
            for item_id, item in st.session_state.carrito.items():
                subtotal = item['precio'] * item['cantidad']
                total_orden += subtotal
                
                c1, c2, c3 = st.columns([4, 2, 2])
                c1.write(f"**{item['nombre']}**\n${item['precio']:.2f}")
                
                cant = c2.number_input("Cant:", min_value=0, value=item['cantidad'], key=f"cant_{item_id}", label_visibility="collapsed")
                if cant != item['cantidad']:
                    if cant == 0:
                        items_a_eliminar.append(item_id)
                    else:
                        st.session_state.carrito[item_id]['cantidad'] = cant
                    st.rerun()
                c3.write(f"**${subtotal:.0f}**")
            
            for item_id in items_a_eliminar:
                del st.session_state.carrito[item_id]
                st.rerun()
                
            st.write("---")
            st.markdown(f"## **Total: ${total_orden:.2f} MXN**")
            
            st.markdown('<div class="boton-cobrar">', unsafe_allow_html=True)
            if st.button("⚡ COBRAR", key="cobrar_orden_final"):
                nueva_venta = {
                    "id_venta": len(st.session_state.historial_ventas) + 1,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "total": total_orden,
                    "productos": list(st.session_state.carrito.values())
                }
                st.session_state.historial_ventas.append(nueva_venta)
                st.session_state.carrito = {} 
                st.success("¡Venta guardada!")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# 5. MÓDULO DE ADMINISTRACIÓN (MÉTRICAS FINANCIERAS)
else:
    password_sistema = st.secrets.get("ADMIN_PASSWORD", "admin123")
    ingreso_pass = st.text_input("Introduce la clave de acceso de administrador:", type="password")
    
    if ingreso_pass == password_sistema:
        st.write("## 📈 Rendimiento Financiero")
        
        ventas_df = pd.DataFrame(st.session_state.historial_ventas)
        if not ventas_df.empty:
            total_ingresos = ventas_df['total'].sum()
            num_transacciones = len(ventas_df)
            ticket_promedio = total_ingresos / num_transacciones
        else:
            total_ingresos = 0.0
            num_transacciones = 0
            ticket_promedio = 0.0
            
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="card-metrica"><p style="color:#E26D27;font-weight:bold;">INGRESOS TOTALES</p><h2>${total_ingresos:.2f}</h2><p>MXN netos</p></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="card-metrica"><p style="color:#E26D27;font-weight:bold;">VENTAS TOTALES</p><h2>{num_transacciones}</h2><p>Tickets cerrados</p></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="card-metrica"><p style="color:#E26D27;font-weight:bold;">TICKET PROMEDIO</p><h2>${ticket_promedio:.2f}</h2><p>Gasto promedio por cliente</p></div>', unsafe_allow_html=True)
            
        st.write("---")
        st.info("💡 El menú estructural está optimizado en código de alto rendimiento. Cuando gustes cambiar los nombres finales de los panes o ajustar precios, solo dime y lo modificamos aquí al instante.")
    elif ingreso_pass != "":
        st.error("Clave incorrecta.")   