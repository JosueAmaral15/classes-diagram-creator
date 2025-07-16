# [] pegar os números 3,4,5,6,7 e 10 para fazer as operações de orientação de estrutura. Se o resto da divisão é as operações aritméticas não derem um desses números, então o default para a estrutura de montagem de um diagrama de classes é 4.

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines
from math import sin, cos, floor, pi

FONTSIZE = 10
SIDES = 4

precision_function = lambda x, expoent: x * floor(0.5 * (abs(x - 10**(-expoent) + 1) - abs(x - 10**(-expoent)) + 1)) - x * floor(0.5 * (abs(x + 10**(-expoent) + 1) - abs(x + 10**(-expoent)) + 1)) + x
angle_radius = lambda x : sin(pi*x/180)
angle_radius_optimized = lambda x: precision_function(angle_radius(x), 6)
angle_radius_cos = lambda x : cos(pi*x/180)
angle_radius_cos_optimized = lambda x: precision_function(angle_radius_cos(x), 6)
depth = 0
# Definição das classes
classes = {
    "FUNC_BENEFICIO_CAD": {
        "attrs": [
            "Cod_Beneficio: Int",
            "Descricao_beneficio: String",
            "Valor_Beneficio: Decimal",
            "Cod_Beneficio: Int",
            "Descricao_beneficio: String",
            "Valor_Beneficio: Decimal",
            "Cod_Beneficio: Int",
            "Descricao_beneficio: String",
            "Valor_Beneficio: Decimal"
        ],
        "pos": (1, 2)
    },
    "FUNC_CAD_EMPREGO": {
        "attrs": [
            "Cod_Tipo_emprego: Int",
            "Tipo_emprego: String"
        ],
        "pos": (1, 0)
    },
    "FUNC_CAD_EST_CIVIL": {
        "attrs": [
            "Cod_Est_civil: Int",
            "Estado_Civil: String?"
        ],
        "pos": (3, 1)
    },
    "FUNC": {
        "attrs": [],
        "pos": (2, 0.8)
    },
    "FUNC_DEP": {
        "attrs": [],
        "pos": (3.2, 2)
    },
    "FUNC_BENEFICIO": {
        "attrs": [],
        "pos": (0, 3)
    }
}

# Relacionamentos
relationships = [
    ("FUNC", "FUNC_CAD_EMPREGO"),
    ("FUNC", "FUNC_CAD_EST_CIVIL"),
    ("FUNC_DEP", "FUNC_CAD_EST_CIVIL"),
    ("FUNC_BENEFICIO", "FUNC_BENEFICIO_CAD"),
]

fig, axes = plt.subplots(figsize=(12, 6))
axes.set_xlim(-1, 5)
axes.set_ylim(-1, 8)
axes.axis("on")


# Desenha as classes
box_width, box_height = 1.6, 0.8
position_left = 0
position_right = SIDES -1
for class_name, class_data in classes.items():
    x, y = class_data["pos"]
    individual_box_height = box_height
    if box_height -0.375 +len(class_data["attrs"]) * FONTSIZE * 0.02 > individual_box_height:
        individual_box_height = box_height +len(class_data["attrs"]) * FONTSIZE * 0.02
        print(f"box_height: {individual_box_height}, class name: {class_name}")
        
    # Caixa da classe
    axes.add_patch(FancyBboxPatch(
        (x, y), box_width, individual_box_height,
        boxstyle="round,pad=0.05", edgecolor="black", facecolor="#e6f2ff"
    ))

    local_title_y = y + individual_box_height - 0.2
    
    #título    
    axes.text(x + 0.05, local_title_y, class_name, fontsize=FONTSIZE, weight="bold", va="top")
    #dados
    for i, attr in enumerate(class_data["attrs"]):
        axes.text(x + 0.05, y +individual_box_height -0.5 - FONTSIZE * 0.02 * i, attr, fontsize=8, va="top")

# Desenha relacionamentos com setas da TABELA FILHA para a PAI
for child, parent in relationships:
    x1, y1 = classes[child]["pos"]
    x2, y2 = classes[parent]["pos"]
    arrow = FancyArrowPatch(
        (x1 + box_width / 2, y1 + box_height / 2),
        (x2 + box_width / 2, y2 + box_height / 2),
        arrowstyle="-|>", mutation_scale=15,
        color="black", linewidth=1.2
    )
    axes.add_patch(arrow)
    # Cardinalidade básica
    axes.text((x1 + x2) / 2 + 0.2, (y1 + y2) / 2 + 0.2, "0..* ➝ 1", fontsize=8, color="gray")

plt.tight_layout()
plt.show()
