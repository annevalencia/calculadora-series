# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:48:43 2026

@author: ane.valencia
"""


## --- IMPORTS ---

import streamlit as st
import math
import random
from datetime import datetime, timedelta


## --- FUNCIONES ---

# Para que puedan meter el tiempo en minutos tanto en enteros como en mm:ss
def tiempo_a_decimal(tiempo_str):
    """Convierte '4:30' o '4' en 4.5"""
    if tiempo_str is None or tiempo_str.strip() == "":
        return None  # Si está vacío, devuelvo None para que la otra función sepa que no hay tiempo
    
    try:
        if ':' in tiempo_str:
            mins, segs = map(int, tiempo_str.split(':'))
            return mins + (segs / 60)
        else:
            return float(tiempo_str)
    except:
        return 0.0 # Valor por defecto si escriben algo raro
    
    
def decimal_a_tiempo(tiempo_dec):
    tiempo_mins = math.trunc(tiempo_dec)
    tiempo_secs_decimal = tiempo_dec - tiempo_mins
    tiempo_secs = int(round(tiempo_secs_decimal*60, 0))
    # if tiempo_secs == 0:
    #     tiempo_secs = '00'
    # tiempo_mmss = ':'.join((str(tiempo_mins), str(tiempo_secs)))
    # return tiempo_mmss
    # El :02d significa: "entero de 2 dígitos, rellena con cero si falta"
    return f"{tiempo_mins}:{tiempo_secs:02d}"
    

# Función cálculo serie
def serie_a_info(mins_serie, dist_serie, ritmo, pendiente=0, n_rep=1):
    """
    Dos opciones: que meta X mins o que meta X kms:
    """
    
    ## RITMO
    ritmo_mins = int(ritmo.split(':')[0])
    ritmo_segs = int(ritmo.split(':')[1])
    ritmo_decimal = ritmo_mins + ritmo_segs/60
    
    
    # Si hay info de mins y kms o no hay de ninguna
    if ((mins_serie is None) & (dist_serie is None)) or ((mins_serie is not None) & (dist_serie is not None)):
        st.error('Mete sólo o la distancia o el tiempo porfi (además del ritmo), que si no igual se vuelve loco :)')
    
    # La serie va por DISTANCIA 
    if mins_serie is None:
        ## TIEMPO
        # Calculo tiempo en función del ritmo y la distancia (* repes)
        mins_total_serie = dist_serie * ritmo_decimal * n_rep
        dist_total_serie = dist_serie * n_rep
        
    # La serie va por TIEMPO
    if dist_serie is None:
        ## DISTANCIA
        # Calculo distancia en función del ritmo y el tiempo (* repes)
        dist_total_serie = mins_serie / ritmo_decimal * n_rep
        mins_total_serie = mins_serie * n_rep
        
    
    ## DESNIVEL ( *10 para que esté en m porque la dist está en km y la pendiente la dejo con el número tal como entra (sin aplicarle el %))
    # dsnivel = dist * pendiente * 10
    desnivel_total_serie = dist_total_serie * pendiente * 10

    return dist_total_serie, mins_total_serie, desnivel_total_serie


# Para obtener la hora en función del lugar
# Poner MADRID o FLORIDA en función de lo que quiera
zona_horaria = 'FLORIDA'
if zona_horaria == 'FLORIDA':
    zona_horaria_txt = 'Florida'
elif zona_horaria == 'MADRID':
    zona_horaria_txt = 'Pamplona'

def obtener_hora_local(zona):
    ahora_utc = datetime.utcnow()    
    if zona == 'FLORIDA':
        # Cabo Cañaveral es UTC-4 (por lo menos para verano)
        return ahora_utc - timedelta(hours=4)
    else:
        # Madrid es UTC+2 en verano (pongo esa)
        return ahora_utc + timedelta(hours=2)


# Enviar saludo en función de la franja horaria
def saludar_segun_hora(hora_h):
    
    # Por la mañana pronto
    if 5 <= hora_h < 11:
        saludos = ["¿Ya te has pegado el madrugón? Madre mía, ¡le echas ganas, eh!",
                   "Mientras otros siguen durmiendo, tú ya has cumplido... ¡de lujooo! 😉",
                   'Dicen que a quien madruga Dios le ayuda... veremos si ha merecido la pena 🤪',
                   'Muy bien el madrugón, todo sea por mejorar para el UD Salinas ⚽']
        
    # Por la mañana tarde (antes de comer)
    elif 11 <= hora_h < 15:
        saludos = ['¡Cumpliendo de buena mañana! Genial, la comida de hoy ya te la has ganado 😜',
                   'Venga, si te salen buenos resultados te habrás ganado el vermutico de antes de comer 🤓']
       
    # Por la tarde pronto
    elif 15 <= hora_h < 18:
        saludos = ["¡Hoooola! ¿Haciendo hueco para la merienda o qué? Venga, que seguro que te la has ganado 🍩",
                   "Espero que el entrenamiento haya sido mejor que la siesta que te estás perdiendo, chaval 😉"]
    
    # Por la tarde tarde
    elif 18 <= hora_h < 23:
        saludos = ["¿Esto qué es, haciendo hueco antes a la caña de rigor? ¿O estamos más de pijama? 🍻😴",
                   "Venga, pégate una duchica que Strava puede esperar unos minutos 🚿"]
        
    # Noche profunda
    else:
        saludos = ['A ver, ¿pero qué horas son estas? ¿Te ha perseguido alguien? 👀',
                   "¡A dormir! Que los ritmos no van a cambiar por mucho que los mires a estas horas 😉"]
    
    return random.choice(saludos)




## --- Inicialización de algunas cosas ---
list_frases_fin = ["Ya puedes estirar bien... 🧘‍♂️",
                   '¡Oleeee! Lo único, tus pobres cuádriceps igual piden la baja 😬',
                   '¡Yujuuuuu! Ahora a esperar lo que realmente querías: kudos 🤠',
                   'Not bad, pero en Strava pon que tenías viento en contra, que si no el ritmo... 😉',
                   '¡Estupendo! Ahora a subir la captura de la frecuencia cardíaca, que queremos ver cómo finges que no has sufrido nada 💔',
                   '¡Estupendo! Ahora a subir la captura de la frecuencia cardíaca, que queremos ver cómo finges que no has sufrido nada 💔',  # la repito porque es mi fav
                   'Muy bien para ser el calentamiento, ¿ahora toca la de verdad? 😜',
                   'Muy bien, pero corriendo en cinta no hay ni viento, ni barro... o sea que así cualquiera 🥱',
                   'Con esto ya estás a puntiiiito de llevarte medalla en la Elorz Trail (pero la de chocolate) 😜',
                   'La verdad que entrenar trail en Florida está jodido, pero oye no desistes... ¡a topeee! 🙂']

# --- INICIALIZACIÓN DE MEMORIA (Sólo se ejecuta una vez al abrir la web) ---
if 'lista_series' not in st.session_state:
    st.session_state.lista_series = []

if 'gracia_cant' not in st.session_state:
    st.session_state.gracia_cant = True

if 'gracia_rit' not in st.session_state:
    st.session_state.gracia_rit = True

if 'gracia_rit_2' not in st.session_state:
    st.session_state.gracia_rit_2 = True                   

if 'gracia_pend' not in st.session_state:
    st.session_state.gracia_pend = True
    
if 'form_id' not in st.session_state:
    st.session_state.form_id = 0

# Saludo (para que se quede fijo y sólo saludo una vez cada vez que entra a la App, si no se genera un saludo nuevo cada vez que se sube una serie)
if 'saludo_fijo' not in st.session_state:
    hora_actual_dt = obtener_hora_local(zona_horaria)
    st.session_state.saludo_fijo = saludar_segun_hora(hora_actual_dt.hour)
    # # Guardo la hora del saludo para la caption
    # st.session_state.hora_caption = f"{hora_actual_dt.hour:02d}:{hora_actual_dt.minute:02d}"
    


#### ----------- APLICACIÓN -----------

# --- OCULTAR MENÚS DE STREAMLIT ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stAppDeployButton {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# --- CONFIGURACIÓN DE LA APP ---

st.set_page_config(page_title="Calculadora de series", page_icon="😎")
# st.title("Calculadora series - resumen")


# Saludo en función de la hora (y el sitio FLORIDA / MADRID
hora_actual_dt = obtener_hora_local(zona_horaria)
hora_h = hora_actual_dt.hour
saludo = saludar_segun_hora(hora_h)


## Creo dos columnas: una muy estrecha para el logo y otra para el título
col1, col2 = st.columns([0.15, 0.85], vertical_alignment="center") 

with col1:
    # Imagen
    st.image("escudo_salinas.png", width = 60)

with col2:
    st.title("Calculadora de series 😎")
    # st.markdown(f'###### {saludo}')
    # Utilizo el saludo guardado en la sesión
    st.write(st.session_state.saludo_fijo)
    
    # Zona y hora en pequeñito
    st.caption(f"{zona_horaria_txt}, {hora_h:02d}:{hora_actual_dt.minute:02d}h")

    
# Inicializamos la lista de series en la "memoria" de la web si no existe
if 'lista_series' not in st.session_state:
    st.session_state.lista_series = []

# --- FORMULARIO DE ENTRADA ---

with st.form("entrada_serie"):
    st.subheader("Serie:")
    c1, c2 = st.columns(2)
    
    with c1:
        # Dos subcolumnas dentro de c1 para mins y dist (para que no me descuadre)
        sub_col1, sub_col2 = st.columns(2)
        
        with sub_col1:
            # Añado KEY dinámica usando el form_id (para después poder limpiar los campos fácilmente)
            mins_input = st.text_input('Minutos:', value= None, help="Rellena este campo si has medido la serie según el tiempo (y no la distancia). Acepta, por ejemplo, tanto los formatos '4:30' (4 mins y medio) como '5' (5 mins)", key=f"mins_{st.session_state.form_id}")
        with sub_col2:
            dist = st.number_input('Kms:', min_value=0.0, value=None, help="Rellena este campo si has medido la serie según la distancia (y no el tiempo). Para los decimales, tienes que usar el punto (.) en vez de la coma", step=0.5, key=f"dist_{st.session_state.form_id}")
            
        # mins = st.number_input('Minutos de la serie:', min_value=1, value=5)
        # dist = st.number_input('Kms de la serie:', min_value=0, value=5)
        ritmo = st.text_input('Ritmo (mins/km):', value=None, help="Acepta el formato mm:ss, por ejemplo: '6:30' o '6:00'", key=f"ritmo_{st.session_state.form_id}")
    with c2:
        pendiente = st.number_input('Pendiente (%):', min_value=0, value=0, key=f"pend_{st.session_state.form_id}")
        n_rep = st.number_input('Número de repeticiones:', min_value=1, value=1, key=f"rep_{st.session_state.form_id}")
    
    ## BOTONES - Añadir y Limpiar
    col_bt1, col_bt2 = st.columns(2)
    with col_bt1:    
        boton_añadir = st.form_submit_button("Añadir serie")
        
    with col_bt2:
        # Este botón "rompe" el form para resetearlo
        boton_limpiar = st.form_submit_button("Limpiar 🧹")


# Si limpian, aumenta el ID y se recarga
if boton_limpiar:
    st.session_state.form_id += 1
    st.rerun()

    
# Al pulsar el botón, se aplica la función "serie_a_info"
if boton_añadir:
    # Si se le ha olvidado meter el ritmo
    if not ritmo: 
        st.warning("¡Sin el ritmo no puedo calcular nada! :(")
    else:
        try:
            # Por si acaso pendiente o n_repes se han quedado vacías (tomo por defecto 0% para la pendiente y 1 para las repes)
            pendiente_final = pendiente if pendiente is not None else 0
            n_rep_final = n_rep if (n_rep is not None and n_rep > 0) else 1
            
            # Convierto tiempo y ritmo de entrada (txt) a decimal
            mins = tiempo_a_decimal(mins_input)
            # if not ritmo.str.contains(':'):
            #     ritmo = ritmo+':00'
            
            dist_s, mins_s, desnivel_s = serie_a_info(mins, dist, ritmo, pendiente_final, n_rep_final)
            
            if dist_s > 0:
                # Guardamos en el diccionario de la sesión
                st.session_state.lista_series.append({
                    'Minutos serie': decimal_a_tiempo(mins_s / n_rep_final),    # tiempo de una sola serie (sin repes)
                    'Repeticiones': n_rep_final,
                    'Minutos totales': decimal_a_tiempo(mins_s),
                    'Ritmo': ritmo,
                    'Pendiente': f'{pendiente_final}%',
                    # Convertimos a f-string para "congelar" los decimales como texto
                    # 'Distancia (km)': f"{dist_s:.2f}", 
                    # 'Desnivel + (m)': f"{desnivel_s:.1f}"
                    'Distancia (km)': dist_s,
                    'Desnivel + (m)': desnivel_s
                })
                
                
                # Tostadas de ánimo/desánimo jejeje (con probabilidad para no saturar)
                try:
                    prob_suerte = 0.5
                    prob_suerte_2 = 0.75
                    # Generación de random (uniforme 0,1)
                    suerte = random.random()
                    
                    # Según ritmo
                    if st.session_state.gracia_rit and suerte < prob_suerte:
                        if int(ritmo.split(':')[0]) >=7:
                            st.toast("Un poco lento...", icon='🐌')
                            st.session_state.gracia_rit = False
                                
                    if st.session_state.gracia_rit_2 and suerte < prob_suerte:
                        if int(ritmo.split(':')[0]) <4:    
                            st.toast('¡Menuda velocidad!', icon='🐆')
                            st.session_state.gracia_rit_2 = False
                        
                    # Según nº series
                    if st.session_state.gracia_cant and suerte < prob_suerte:
                        if len(st.session_state.lista_series) > 6:
                            st.toast(f"¡Madre mía cuántas series!", icon = '😯')
                            st.session_state.gracia_cant = False
                            
                    # Según pendiente (si es 12% o más)
                    if st.session_state.gracia_pend and pendiente_final >= 12 and suerte < prob_suerte_2:
                        frases_pendiente = [f"¿Al {pendiente_final}%? No sabía que derrepente le hacías competencia a Kilian 😗",
                                            f"¿{pendiente_final}%? Joder, eso en Cabo Cañaberal tiene que estar considerado ya alta montaña..."]
                        # Warning para que destaque más que un toast (que si no se va muy rápido)
                        st.warning(random.choice(frases_pendiente))
                        st.session_state.gracia_pend = False
                                
                except:
                    pass
                
                # RESUMEN DE LA SERIE
                st.success(f"Serie añadida: {round(dist_s, 2)} km al {pendiente_final}%, {decimal_a_tiempo(mins_s)} mins ({ritmo}/km) y +{round(desnivel_s, 1)} m")
                
                
            else:
                st.warning('Mete información sobre la distancia o el tiempo porfi :) ¡si no, no se puede calcular nada!')
        except Exception as e:
            st.error("Algo has metido mal!!!")


# --- MOSTRAR RESULTADOS ---
if st.session_state.lista_series:
    st.divider()
    st.subheader("Resumen de series acumuladas:")
    
    # Muestra tabla con lo que llevamos hasta ahora
    st.table(st.session_state.lista_series)
    
    # --- NUEVA SECCIÓN PARA ELIMINAR ---
    with st.expander("No te preocupes si te has equivocado en algo, puedes eliminar series aquí:"):
        # Creamos una lista de etiquetas para el selector (ej: "Serie 1", "Serie 2"...)
        opciones = [f"Serie {i}" for i in range(len(st.session_state.lista_series))]
        serie_a_borrar = st.selectbox("Elige cuál quieres borrar (fíjate en el índice de la izquierda de la tabla) y después dale a 'Eliminar serie':", opciones)
        
        if st.button("Eliminar serie"):
            # Obtenemos el índice (Serie 1 es índice 0)
            indice = opciones.index(serie_a_borrar)
            # Borramos de la lista
            st.session_state.lista_series.pop(indice)
            st.toast(f"¡{serie_a_borrar} eliminada!")
            st.rerun() # Refrescamos para que desaparezca de la tabla


    ## CÁLCULO DE GLOBALES
    mins_total = sum(tiempo_a_decimal(s['Minutos totales']) for s in st.session_state.lista_series)
    dist_total = sum(s['Distancia (km)'] for s in st.session_state.lista_series)
    desnivel_total = int(round(sum(s['Desnivel + (m)'] for s in st.session_state.lista_series), 0))
    
    # Ritmo medio = tiempo total / distancia total 
    if dist_total > 0:
        ritmo_medio = mins_total / dist_total
        ritmo_mins_f = math.trunc(ritmo_medio)
        ritmo_secs_decimal = ritmo_medio - ritmo_mins_f
        ritmo_secs_f = round(ritmo_secs_decimal * 60, 0)
        
        # Formatear segundos para que siempre tengan dos dígitos (ej: 05 en vez de 5)
        ritmo_medio_mmss = f"{ritmo_mins_f}:{int(ritmo_secs_f):02d}"
    else:
        ritmo_medio_mmss = "00:00"
        
    # Texto para tiempo total (en función de si es más o menos de 1h)
    # si es más de 1h  --> __h, __m
    if mins_total >= 60:
        tiempo_total_horas = int(mins_total // 60)
        tiempo_total_mins = int(mins_total % 60)        
        
        if tiempo_total_mins == 0:
            txt_tiempo_mins = ''
        else:
            txt_tiempo_mins  = f'{tiempo_total_mins:02d}m'
            
        # txt_tiempo_total = f'{tiempo_horas}h {tiempo_mins}min'
        txt_tiempo_total = f"{tiempo_total_horas}h {txt_tiempo_mins}"
    
    # si es menos de 1h  --> __m, __s           
    else:
        tiempo_total_mins = int(math.trunc(mins_total))
        tiempo_total_sec = int(round((mins_total - tiempo_total_mins)*60, 0))
        
        # Por limpieza, si los segundos son 0, que aparezcan sólo los minutos
        if tiempo_total_sec == 0:
            txt_tiempo_segundos = ''
        else:
            txt_tiempo_segundos = f'{tiempo_total_sec:02d}s'

        txt_tiempo_total = f"{tiempo_total_mins}min {txt_tiempo_segundos}"
        
    # BOTÓN PARA RESUMEN
    if st.button("RESUMEN FINAL"):
        
        # Resumen visual
        if desnivel_total >= 1000:
            frases_cima = ['¡¡1000m!! Ojito que a esa altura ya empieza a fatar el oxígeno 🥴',
                           '¡¡+1000m en cinta!! Enhorabuena😘']
            st.snow()
            st.toast(random.choice(frases_cima))
        else:
            st.balloons()
        
        st.header("🤩 RESUMEN ")
        col1, col2, col3, col4 = st.columns(4)
        # col1.metric("Tiempo", f"{decimal_a_tiempo(mins_total)} min")
        col1.metric("Tiempo", f"{txt_tiempo_total}")
        col2.metric("Distancia", f"{dist_total:.2f} km")
        col3.metric("Ritmo medio", f"{ritmo_medio_mmss} /km")
        col4.metric("Desnivel", f"+{desnivel_total} m")
        
        # Frase final al azar
        frase_fin = random.choice(list_frases_fin)
        st.markdown(f"---") # Una línea divisoria antes del mensaje final
        st.markdown(f"<p style='font-style: italic; color: #b8ffe0; text-align: center; font-size: 18px;'>{frase_fin}</p>", unsafe_allow_html=True)
        
    # Botón para borrar y empezar de nuevo
    if st.button("Borrar todo"):
        st.session_state.lista_series = []
        # Resetear también las gracias para que puedan volver a salir
        st.session_state.gracia_cant = True
        st.session_state.gracia_rit = True
        st.session_state.gracia_rit_2 = True
        st.session_state.gracia_pend = True
        st.rerun()
