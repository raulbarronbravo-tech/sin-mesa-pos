import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE LA PÁGINA Y MARCA
st.set_page_config(page_title="SIN MESA - POS", layout="wide", initial_sidebar_state="collapsed")

# Estilos visuales con Verde Quimera, Naranja Zumo y fondo Crema Rústico
st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7; } 
    h1, h2, h3 { color: #155E3B !important; font-family: 'Arial Black', sans-serif; } 
    .stButton>button {
        background-color: #155E3B; color: white; border-radius: 12px; font-weight: bold;
        padding: 12px; width: 100%; border: none; transition: 0.3s; font-size: 14px;
    }
    .stButton>button:hover { background-color: #E26D27; color: white; } 
    .boton-cobrar>div>button { background-color: #E26D27 !important; color: white !important; font-size: 20px !important; padding: 20px !important; }
    .card-metrica {
        background-color: white; border: 2px solid #155E3B; border-radius: 15px;
        padding: 20px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    /* Contenedor flotante para el personaje animado en la esquina inferior izquierda */
    .personaje-flotante {
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 99;
        pointer-events: none;
    }
    </style>
""", unsafe_allow_html=True)

# 2. BASE DE DATOS INICIAL DEL MENÚ REAL (Basado en la imagen del menú)
if 'menu' not in st.session_state:
    st.session_state.menu = [
        # --- EXPRESO ---
        {"id": 1, "nombre": "Expreso Sencillo", "categoria": "Café", "precio": 26.0},
        {"id": 2, "nombre": "Expreso Doble", "categoria": "Café", "precio": 36.0},
        {"id": 3, "nombre": "Expreso Macchiato", "categoria": "Café", "precio": 38.0},
        {"id": 4, "nombre": "Expreso Tonic (16oz)", "categoria": "Café", "precio": 46.0},
        
        # --- CAFÉ CLÁSICO (8oz, 12oz, 16oz) ---
        {"id": 5, "nombre": "Capuchino 8oz", "categoria": "Café", "precio": 45.0},
        {"id": 6, "nombre": "Capuchino 12oz", "categoria": "Café", "precio": 55.0},
        {"id": 7, "nombre": "Capuchino Frío 16oz", "categoria": "Café", "precio": 65.0},
        
        {"id": 8, "nombre": "Latte 8oz", "categoria": "Café", "precio": 45.0},
        {"id": 9, "nombre": "Latte 12oz", "categoria": "Café", "precio": 55.0},
        {"id": 10, "nombre": "Latte Frío 16oz", "categoria": "Café", "precio": 65.0},
        
        {"id": 11, "nombre": "Moka 8oz", "categoria": "Café", "precio": 45.0},
        {"id": 12, "nombre": "Moka 12oz", "categoria": "Café", "precio": 55.0},
        {"id": 13, "nombre": "Moka Frío 16oz", "categoria": "Café", "precio": 65.0},
        
        {"id": 14, "nombre": "Flat White 8oz", "categoria": "Café", "precio": 45.0},
        {"id": 15, "nombre": "Flat White 12oz", "categoria": "Café", "precio": 55.0},
        
        {"id": 16, "nombre": "Americano 8oz", "categoria": "Café", "precio": 40.0},
        {"id": 17, "nombre": "Americano 12oz", "categoria": "Café", "precio": 50.0},
        {"id": 18, "nombre": "Americano Frío 16oz", "categoria": "Café", "precio": 65.0},
        
        # --- COLD BREW (16oz) ---
        {"id": 19, "nombre": "Cold Brew Tonic", "categoria": "Cold Brew", "precio": 69.0},
        {"id": 20, "nombre": "Cold Brew Mineral", "categoria": "Cold Brew", "precio": 69.0},
        {"id": 21, "nombre": "Cold Brew Guayaba", "categoria": "Cold Brew", "precio": 69.0},
        {"id": 22, "nombre": "Cold Brew Mango", "categoria": "Cold Brew", "precio": 69.0},
        
        # --- CAPUCHINOS CON SABOR ---
        {"id": 23, "nombre": "Capuchino Menta 8oz", "categoria": "Café con Sabor", "precio": 50.0},
        {"id": 24, "nombre": "Capuchino Menta 12oz", "categoria": "Café con Sabor", "precio": 60.0},
        {"id": 25, "nombre": "Capuchino Menta Frío 16oz", "categoria": "Café con Sabor", "precio": 69.0},
        
        {"id": 26, "nombre": "Capuchino Vainilla 8oz", "categoria": "Café con Sabor", "precio": 50.0},
        {"id": 27, "nombre": "Capuchino Vainilla 12oz", "categoria": "Café con Sabor", "precio": 60.0},
        {"id": 28, "nombre": "Capuchino Vainilla Frío 16oz", "categoria": "Café con Sabor", "precio": 69.0},
        
        {"id": 29, "nombre": "Capuchino Caramelo 8oz", "categoria": "Café con Sabor", "precio": 50.0},
        {"id": 30, "nombre": "Capuchino Caramelo 12oz", "categoria": "Café con Sabor", "precio": 60.0},
        {"id": 31, "nombre": "Capuchino Caramelo Frío 16oz", "categoria": "Café con Sabor", "precio": 69.0},
        
        {"id": 32, "nombre": "Capuchino Crema Irlandesa 8oz", "categoria": "Café con Sabor", "precio": 50.0},
        {"id": 33, "nombre": "Capuchino Crema Irlandesa 12oz", "categoria": "Café con Sabor", "precio": 60.0},
        {"id": 34, "nombre": "Capuchino Crema Irlandesa Frío 16oz", "categoria": "Café con Sabor", "precio": 69.0},
        
        # --- BATIDOS DE PROTEÍNA (16oz) ---
        {"id": 35, "nombre": "Batido Proteína Fresa", "categoria": "Batidos", "precio": 64.0},
        {"id": 36, "nombre": "Batido Proteína Plátano", "categoria": "Batidos", "precio": 64.0},
        {"id": 37, "nombre": "Batido Proteína Fresa + Plátano", "categoria": "Batidos", "precio": 75.0}
    ]

if 'carrito' not in st.session_state: st.session_state.carrito = {}
if 'historial_ventas' not in st.session_state: st.session_state.historial_ventas = []

# 3. ENCABEZADO SUPERIOR DE LA APP
col_logo, col_nav = st.columns([2, 1])
with col_logo:
    st.title("☕ SIN MESA")
    st.subheader("Punto de Venta Oficial")
with col_nav:
    modo = st.radio("Panel de Control:", ["Ventas (Barra)", "Administrador"], horizontal=True)

st.write("---")

# 4. SISTEMA DE VENTAS TÁCTIL
if modo == "Ventas (Barra)":
    col_izq, col_der = st.columns([5, 3])
    
    with col_izq:
        st.write("### 🛍️ Categorías")
        # Pestañas basadas exactamente en tu menú físico
        categoria_sel = st.tabs(["Todos", "Café", "Café con Sabor", "Cold Brew", "Batidos"])
        
        def mostrar_botones(cat_filtro=None):
            productos_filtrados = [p for p in st.session_state.menu if cat_filtro is None or p["categoria"] == cat_filtro]
            cols_grid = st.columns(3) # Cuadrícula de 3 columnas para botones grandes en tablet
            for i, prod in enumerate(productos_filtrados):
                col_btn = cols_grid[i % 3]
                with col_btn:
                    if st.button(f"{prod['nombre']}\n${prod['precio']:.2f} MXN", key=f"btn_{prod['id']}"):
                        p_id = prod['id']
                        if p_id in st.session_state.carrito:
                            st.session_state.carrito[p_id]['cantidad'] += 1
                        else:
                            st.session_state.carrito[p_id] = {'nombre': prod['nombre'], 'precio': prod['precio'], 'cantidad': 1}
                        st.rerun()

        with categoria_sel[0]: mostrar_botones()
        with categoria_sel[1]: mostrar_botones("Café")
        with categoria_sel[2]: mostrar_botones("Café con Sabor")
        with categoria_sel[3]: mostrar_botones("Cold Brew")
        with categoria_sel[4]: mostrar_botones("Batidos")

        # LOGICA PARA INTEGRAR EL PERSONAJE ANIMADO
        # Si pones tu personaje sin fondo crema en la carpeta con el nombre 'personaje.png', se cargará abajo automáticamente
        if os.path.exists("personaje.png"):
            st.markdown('<div class="personaje-flotante">', unsafe_allow_html=True)
            st.image("personaje.png", width=120)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        st.write("### 🛒 Orden de Cobro")
        if not st.session_state.carrito:
            st.info("Agrega productos tocando los botones de la izquierda.")
        else:
            total_orden = 0.0
            items_a_eliminar = []
            
            for p_id, item in st.session_state.carrito.items():
                subtotal = item['precio'] * item['cantidad']
                total_orden += subtotal
                
                c1, c2, c3 = st.columns([4, 2, 2])
                c1.write(f"**{item['nombre']}**\n${item['precio']:.2f}")
                
                cant = c2.number_input("Cant:", min_value=0, value=item['cantidad'], key=f"cant_{p_id}", label_visibility="collapsed")
                if cant != item['cantidad']:
                    if cant == 0:
                        items_a_eliminar.append(p_id)
                    else:
                        st.session_state.carrito[p_id]['cantidad'] = cant
                    st.rerun()
                c3.write(f"**${subtotal:.2f}**")
            
            for p_id in items_a_eliminar:
                del st.session_state.carrito[p_id]
                st.rerun()
                
            st.write("---")
            st.markdown(f"## **Total: ${total_orden:.2f} MXN**")
            
            st.markdown('<div class="boton-cobrar">', unsafe_allow_html=True)
            if st.button("⚡ REGISTRAR VENTA", key="cobrar_orden"):
                nueva_venta = {
                    "id_venta": len(st.session_state.historial_ventas) + 1,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "total": total_orden,
                    "productos": list(st.session_state.carrito.values())
                }
                st.session_state.historial_ventas.append(nueva_venta)
                st.session_state.carrito = {} 
                st.success("¡Cobro guardado con éxito!")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# 5. MÓDULO DE ADMINISTRACIÓN (MÉTRICAS DEL NEGOCIO Y EDITOR)
else:
    password_sistema = st.secrets.get("ADMIN_PASSWORD", "admin123")
    ingreso_pass = st.text_input("Introduce la clave de acceso financiera:", type="password")
    
    if ingreso_pass == password_sistema:
        st.write("## 📈 Control de Ventas y Ticket Promedio")
        
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
            st.markdown(f'<div class="card-metrica"><p style="color:#E26D27;font-weight:bold;">TRANSACCIONES</p><h2>{num_transacciones}</h2><p>Ventas concretadas</p></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="card-metrica"><p style="color:#E26D27;font-weight:bold;">TICKET PROMEDIO</p><h2>${ticket_promedio:.2f}</h2><p>Dinero promedio por cliente</p></div>', unsafe_allow_html=True)

        st.write("---")
        st.write("## 📝 Añadir o Modificar Productos del Menú")
        
        with st.form("nuevo_producto_form", clear_on_submit=True):
            st.write("### Crear nuevo artículo")
            nom_p = st.text_input("Nombre de la bebida, batido o pan:")
            cat_p = st.selectbox("Categoría asignada:", ["Café", "Café con Sabor", "Cold Brew", "Batidos"])
            prec_p = st.number_input("Precio final (MXN):", min_value=1.0, value=45.0)
            
            if st.form_submit_button("Guardar en Sistema"):
                if nom_p:
                    nuevo_id = max([p["id"] for p in st.session_state.menu]) + 1 if st.session_state.menu else 1
                    st.session_state.menu.append({"id": nuevo_id, "nombre": nom_p, "categoria": cat_p, "precio": prec_p})
                    st.success(f"Se agregó '{nom_p}' exitosamente.")
                    st.rerun()

        st.write("### Lista del Menú Vigente en la Barra")
        menu_df = pd.DataFrame(st.session_state.menu)
        st.dataframe(menu_df[['categoria', 'nombre', 'precio']], use_container_width=True)