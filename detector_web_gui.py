import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext, messagebox 

#Poryecto realizado hace 4 años atrás para el instituto CPS (modificado recientemente para compartirlo en GH)
#=====
#analizador BACKEND 
#----------------------------
def detectar_backend(headers, cookies, url):
    resultados = []
    confianza = 0 #esto es hiper-subjetivo

	#===PRECONFIGURACIONES===
    powered = headers.get("X-Powered-By", "").lower()
    server = headers.get("Server", "").lower()

    if "php" in powered or ".php" in url:
        resultados.append("PHP → detectado por X-Powered-By o URL")
        confianza += 40

    if "asp.net" in powered or "asp.net" in server:
        resultados.append("ASP.NET → detectado por headers")
        confianza += 40

    if "express" in powered:
        resultados.append("Node.js (Express) → X-Powered-By")
        confianza += 40

    if "sessionid" in cookies:
        resultados.append("Python (Django) → cookie sessionid")
        confianza += 30

    if not resultados:
        resultados.append(
	"No detectado -> el sitiono NO expone headers, cookies ni pistas claras."
	"Esto es común en sitios grandes, CDNs o infraestructuras privadas."
        )
        confianza = 20

    return resultados, min(confianza, 100)


#=====
#analizador FRONTEND
#----------------------------
def detectar_frontend(html):
    resultados = []
    confianza = 0
    html_lower = html.lower()

    if "react" in html_lower:
        resultados.append("React → palabra clave encontrada en HTML/JS")
        confianza += 40

    if "angular" in html_lower or "ng-app" in html_lower:
        resultados.append("Angular → atributos ng-")
        confianza += 40

    if "vue" in html_lower or "data-v-" in html_lower:
        resultados.append("Vue → atributos data-v-")
        confianza += 40

    if not resultados:
        resultados.append("HTML / JavaScript clásico")
        confianza = 30 #subjetivo

    return resultados, min(confianza, 100)


#=====
#FUNCIÓN PRINCIPAL
#----------------------------
def analizar_url():
    url = entrada_url.get().strip()
    salida.delete("1.0", tk.END)

    if not url.startswith("http"):
        salida.insert(tk.END, "⚠ Ingresá una URL válida con http o https\n")
        return

    salida.insert(tk.END, "Analizando...\n\n")

    try:
        r = requests.get(url, timeout=6)
        html = r.text
        headers = r.headers
        cookies = r.cookies.get_dict()

        backend, conf_back = detectar_backend(headers, cookies, url)
        frontend, conf_front = detectar_frontend(html)

        salida.insert(tk.END, "============================\n")
        salida.insert(tk.END, "RESULTADO DEL ANÁLISIS\n")
        salida.insert(tk.END, "============================\n\n")

        salida.insert(tk.END, f"HTTP Status: {r.status_code}\n\n")

        salida.insert(tk.END, "🔧 BACKEND PROBABLE:\n")
        for b in backend:
            salida.insert(tk.END, f" - {b}\n")
        salida.insert(tk.END, f"Confianza backend: {conf_back}%\n\n")

        salida.insert(tk.END, "🎨 FRONTEND PROBABLE:\n")
        for f in frontend:
            salida.insert(tk.END, f" - {f}\n")
        salida.insert(tk.END, f"Confianza frontend: {conf_front}%\n")

    except Exception as e:
        salida.insert(tk.END, f"❌ Error al analizar la URL:\n{e}")


def mostrar_info():
    mensaje = (
        "DetectiveDeCodigo\n\n"
        "¿Cómo funciona?\n"
        "- Analiza headers HTTP públicos\n"
        "- Revisa cookies visibles\n"
        "- Examina el HTML y JavaScript\n\n"
        "Limitaciones:\n"
        "- No puede ver el código del servidor\n"
        "- Muchos sitios ocultan su backend (CDN, proxies)\n"
        "- Los resultados son estimaciones, no certezas\n\n"
        "Si aparece 'No detectado', significa que\n"
        "no hubo pistas suficientes para inferir la tecnología."
    )

    messagebox.showinfo("ℹ️ Información", mensaje)

#=====
#GUI (CYBERPUNK)
#----------------------------
ventana = tk.Tk()
ventana.title("DetectiveDeCodigo // MODO CYBERPUNK ")
ventana.geometry("720x520")
ventana.configure(bg="#0b0f14")  # fondo oscuro

#Fuente estilo terminal
fuente_titulo = ("Consolas", 12, "bold")
fuente_texto = ("Consolas", 10)

#Título
tk.Label(
    ventana,
    text=">> DetectiveDeCodigo v2.0",
    bg="#0b0f14",
    fg="#00ff9c",
    font=fuente_titulo
).pack(pady=10)

#Label URL
tk.Label(
    ventana,
    text="Ingresá una URL:",
    bg="#0b0f14",
    fg="#00e5ff",
    font=fuente_texto
).pack(pady=5)

#Entrada URL
entrada_url = tk.Entry(
    ventana,
    width=60,
    bg="#111827",
    fg="#00ff9c",
    insertbackground="#00ff9c",
    font=fuente_texto,
    relief="flat"
)
entrada_url.pack(pady=5)

boton_info = tk.Button(
    ventana,
    text="ℹ️ INFO",
    command=mostrar_info,
    font=fuente_texto,
    relief="flat",
    padx=8
)
boton_info.pack(pady=5)

#Botón analizar
tk.Button(
    ventana,
    text="ANALIZAR",
    command=analizar_url,
    bg="#00ff9c",
    fg="#0b0f14",
    activebackground="#00e5ff",
    font=fuente_texto,
    relief="flat",
    padx=10,
    pady=5
).pack(pady=12)

#Área de salida tipo terminal
salida = scrolledtext.ScrolledText(
    ventana,
    wrap=tk.WORD,
    bg="#020617",
    fg="#00ff9c",
    insertbackground="#00ff9c",
    font=fuente_texto,
    relief="flat"
)
salida.pack(expand=True, fill="both", padx=12, pady=12)


ventana.bind("<Return>", lambda event: analizar_url())

ventana.mainloop()
