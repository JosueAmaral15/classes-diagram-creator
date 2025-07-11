import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

# Dados simulados
textos = [
    ax.text(10, 20, "Primeiro"),
    ax.text(50, 50, "Segundo"),
    ax.text(80, 30, "Alvo"),
]

# Campo de texto
axbox = plt.axes([0.2, 0.05, 0.6, 0.075])  # [left, bottom, width, height]
text_box = TextBox(axbox, "Buscar texto:")

# Callback de busca
def buscar_texto(valor):
    valor = valor.strip().lower()

    for t in textos:
        if valor in t.get_text().lower():
            x, y = t.get_position()
            w, h = 20, 20
            ax.set_xlim(x - w/2, x + w/2)
            ax.set_ylim(y - h/2, y + h/2)
            fig.canvas.draw_idle()
            return

    print("Texto não encontrado:", valor)

# Vincula a função ao evento de entrada
text_box.on_submit(buscar_texto)

# Mostra
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
plt.show()
