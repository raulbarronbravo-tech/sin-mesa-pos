import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA Y MARCA
st.set_page_config(page_title="SIN MESA - POS", layout="wide", initial_sidebar_state="collapsed")

# Colores institucionales aplicados vía CSS inyectado
st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7; } /* Fondo Crema suave Rústico */
    h1, h2, h3 { color: #155E3B !important; font-family: 'Arial Black', sans-serif; } /* Verde Quimera */
    .stButton>button {
        background-color: #155E3B; color: white; border-radius: 12px; font-weight: bold;
        padding: 15px; width: 100%; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #E26D27; color: white; } /* Cambio a Naranja Zumo */
    .boton-cobrar>div>button { background-color: #E26D27 !important; color: white !important; font-size: 20px !important; }
    .card-metrica {
        background-color: white; border: 2px solid #155E3B; border-radius: 15px;
        padding: 20px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 2. INICIALIZACIÓN DE DATOS LOCALES (MEMORIA TEMPORAL DE SESIÓN)
if 'menu' not in st.session_state:
    st.session_state.menu = [
        {"id": 1, "nombre": "Café Americano", "categoria": "Café", "precio": 45.0},
        {"id": 2, "nombre": "Espresso", "categoria": "Café", "precio": 40.0},
        {"id": 3, "nombre": "Capuccino", "categoria": "Café", "precio": 55.0},
        {"id": 4, "nombre": "Concha de Vainilla", "categoria": "Pan", "precio": 35.0},
        {"id": 5, "nombre": "Croissant de Mantequilla", "categoria": "Pan", "precio": 45.0},
        {"id": 6, "nombre": "Batido de Proteína Vainilla", "categoria": "Batidos", "precio": 75.0},
        {"id": 7, "nombre": "Batido de Proteína Plátano", "categoria": "Batidos", "precio": 75.0}
    ]

if 'carrito' not in st.session_state: st.session_state.carrito = {}
if 'historial_ventas' not in st.session_state: st.session_state.historial_ventas = []

# 3. BARRA NAVEGACIÓN SUPERIOR
col_logo, col_nav = st.columns([2, 1])
with col_logo:
    st.title("☕ SIN MESA")
    st.subheader("Café, Pan y Batidos de Proteína")
with col_nav:
    modo = st.radio("Panel:", ["Ventas (Barra)", "Administrador"], horizontal=True)

st.write("---")

# 4. MÓDULO DE VENTAS (INTERFAZ DE LA TABLETA)
if modo == "Ventas (Barra)":
    col_izq, col_der = st.columns([5, 3])
    
    with col_izq:
        st.write("### 🛍️ Selecciona los Productos")
        categoria_sel = st.tabs(["Todos", "Café", "Pan", "Batidos"])
        
        def mostrar_botones(cat_filtro=None):
            productos_filtrados = [p for p in st.session_state.menu if cat_filtro is None or p["categoria"] == cat_filtro]
            # Grid táctil de 3 columnas
            cols_grid = st.columns(3)
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
        with categoria_sel[2]: mostrar_botones("Pan")
        with categoria_sel[3]: mostrar_botones("Batidos")

    with col_der:
        st.write("### 🛒 Orden Actual")
        if not st.session_state.carrito:
            st.info("El carrito está vacío. Agrega productos de la izquierda.")
        else:
            total_orden = 0.0
            items_a_eliminar = []
            
            for p_id, item in st.session_state.carrito.items():
                subtotal = item['precio'] * item['cantidad']
                total_orden += subtotal
                
                c1, c2, c3 = st.columns([4, 2, 2])
                c1.write(f"**{item['nombre']}**\n${item['precio']:.2f}")
                
                # Control de cantidad incremental rápido (+/-)
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
            
            # Botón Naranja Zumo para cobrar
            st.markdown('<div class="boton-cobrar">', unsafe_allow_html=True)
            if st.button("⚡ COBRAR Y REGISTRAR", key="cobrar_orden"):
                nueva_venta = {
                    "id_venta": len(st.session_state.historial_ventas) + 1,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "total": total_orden,
                    "productos": list(st.session_state.carrito.values())
                }
                st.session_state.historial_ventas.append(nueva_venta)
                st.session_state.carrito = {} # Limpiar pantalla para el siguiente cliente
                st.success("¡Venta registrada con éxito!")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# 5. MÓDULO DE ADMINISTRACIÓN (TICKET PROMEDIO Y EDICIÓN DE MENÚ)
else:
    # Sistema de seguridad básico con la contraseña guardada en "Secretos"
    password_sistema = st.secrets.get("ADMIN_PASSWORD", "admin123")
    ingreso_pass = st.text_input("Introduce la clave de acceso de administrador:", type="password")
    
    if ingreso_pass == password_sistema:
        st.write("## 📈 Rendimiento del Negocio")
        
        # CÁLCULOS FINANCIEROS DEL TICKET PROMEDIO
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
            st.markdown(f'<div class="card-metrica"><p style="color:#E26D27;font-weight:bold;">TICKET PROMEDIO</p><h2>${ticket_promedio:.2f}</h2><p>Por cliente diario</p></div>', unsafe_allow_html=True)

        st.write("---")
        st.write("## 📝 Editor del Menú de Productos")
        
        # Formulario para agregar nuevos productos
        with st.form("nuevo_producto_form", clear_on_submit=True):
            st.write("### Agregar un nuevo producto al Menú")
            nom_p = st.text_input("Nombre del producto (Ej: Batido Fresa Pro):")
            cat_p = st.selectbox("Categoría:", ["Café", "Pan", "Batidos"])
            prec_p = st.number_input("Precio de venta (MXN):", min_value=1.0, value=20.0)
            
            if st.form_submit_button("Guardar en Menú"):
                if nom_p:
                    nuevo_id = max([p["id"] for p in st.session_state.menu]) + 1 if st.session_state.menu else 1
                    st.session_state.menu.append({"id": nuevo_id, "nombre": nom_p, "categoria": cat_p, "precio": prec_p})
                    st.success(f"'{nom_p}' se agregó al menú correctamente.")
                    st.rerun()
                else:
                    st.error("El nombre del producto no puede estar vacío.")

        # Tabla del menú actual con opción de borrar
        st.write("### Menú Vigente")
        menu_df = pd.DataFrame(st.session_state.menu)
        st.dataframe(menu_df[['categoria', 'nombre', 'precio']], use_container_width=True)
    
    elif ingreso_pass != "":
        st.error("Clave incorrecta. Acceso denegado al módulo financiero.")