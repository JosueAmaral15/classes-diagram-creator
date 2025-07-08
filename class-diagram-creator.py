# [] pegar os números 3,4,5,6,7 e 10 para fazer as operações de orientação de estrutura. Se o resto da divisão é as operações aritméticas não derem um desses números, então o default para a estrutura de montagem de um diagrama de classes é 4.

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines
from math import sin, cos, floor, pi

class Controller:
    def __init__(self, classes, relationships):
        
        #constants
        self.BOX_WIDTH_DEFAULT, self.BOX_HEIGHT_DEFAULT = 1.6, 0.8
        self.FONTSIZE = 10
        self.SIDES = 4
        
        #functions
        self.precision_function = lambda x, expoent: x * floor(0.5 * (abs(x - 10**(-expoent) + 1) - abs(x - 10**(-expoent)) + 1)) - x * floor(0.5 * (abs(x + 10**(-expoent) + 1) - abs(x + 10**(-expoent)) + 1)) + x
        self.angle_radius_sin = lambda x : sin(pi*x/180)
        self.angle_radius_sin_optimized = lambda x: self.precision_function(self.angle_radius_sin(x), 6)
        self.angle_radius_cos = lambda x : cos(pi*x/180)
        self.angle_radius_cos_optimized = lambda x: self.precision_function(self.angle_radius_cos(x), 6)
        
        #objects
        self.classes = classes
        self.relationships = relationships
        
        #numbers
        self.total_length = len(self.classes)
        self.max_depth = self.calculate_greater_area(self.classes)**(2**(self.total_length//self.SIDES))
        
        for classes_name in self.classes.keys():
            self.classes[classes_name]["width"] = self.BOX_WIDTH_DEFAULT
            self.classes[classes_name]["height"] = self.BOX_HEIGHT_DEFAULT
            self.classes[classes_name]["angle"] = 0
        
        fig, self.axes = plt.subplots(figsize=(12, 6))
        self.axes.set_xlim(-3, 10)
        self.axes.set_ylim(-3, 8)
        self.axes.axis("on")

    def _draw_box(self, class_name, class_data, x, y, box_width, box_height, edge_color="black", face_color="#e6f2ff"):
        class_data["pos"] = (x,y)
        if box_height -0.375 +len(class_data["attrs"]) * self.FONTSIZE * 0.02 > box_height:
            box_height = box_height +len(class_data["attrs"]) * self.FONTSIZE * 0.02
            class_data["height"] = box_height
            
        box_width = max(max(self.larger_string_size_list(class_data["attrs"]), len(class_name)) * self.FONTSIZE * 0.0035, self.BOX_WIDTH_DEFAULT)
        class_data["width"] = box_width
        #print(f"box_height: {box_height}, class name: {class_name}")
            
        # Caixa da classe
        self.axes.add_patch(FancyBboxPatch(
            (x, y), box_width, box_height,
            boxstyle="round,pad=0.05", edgecolor=edge_color, facecolor=face_color
        ))

        #título    
        local_title_y = y + box_height - 0.2
        self.axes.text(x + 0.05, local_title_y, class_name, fontsize=self.FONTSIZE, weight="bold", va="top")
        
        #dados
        for i, attr in enumerate(class_data["attrs"]):
            self.axes.text(x + 0.05, y +box_height -0.5 - self.FONTSIZE * 0.02 * i, attr, fontsize=8, va="top")

    def _draw_box_recursively(self, count, depth, subclasses, sides, box_width, box_height, edge_color="black", face_color="#e6f2ff"):
        if count != sides:
            angle = count*(360//sides)
            x,y = self.angle_radius_sin_optimized(angle)*depth, self.angle_radius_cos_optimized(angle)*depth
            subclass = dict(list(subclasses.items())[count:count+1])
            for class_name, class_data in subclass.items():
                class_data["angle"] = angle
                self._draw_box(class_name, class_data, x, y, box_width, box_height, edge_color, face_color)
            self._draw_box_recursively(count +1, depth, subclasses, sides, box_width, box_height, edge_color, face_color)
        else:
            return
        

    def _draw_relationship(self, child, parent, classes):
        # Desenha relacionamentos com setas da TABELA FILHA para a PAI
        x1, y1 = self.classes[child]["pos"]
        x2, y2 = self.classes[parent]["pos"]
        box_width_child = classes[child]["width"]
        box_height_child = classes[child]["height"]
        box_width_parent = classes[parent]["width"]
        box_height_parent = classes[parent]["height"]
        child_sin = self.angle_radius_sin_optimized(self.classes[child]["angle"])
        child_cos = self.angle_radius_cos_optimized(self.classes[child]["angle"])
        parent_sin = self.angle_radius_sin_optimized(self.classes[parent]["angle"])
        parent_cos = self.angle_radius_cos_optimized(self.classes[parent]["angle"])
        child_x = x1+(((box_width_child if child_sin != 0 else (box_width_child/2)) if child_sin >= 0 else 0) if child_cos != 0 else (box_width_child if child_sin < 0 else 0))
        child_y = y1+(((box_height_child if child_cos != 0 else (box_height_child/2)) if child_cos <= 0 else 0) if child_sin >= 0 else box_height_child/2)
        parent_x = x2+(((box_width_parent if parent_sin != 0 else (box_width_parent/2)) if parent_sin >= 0 else 0) if parent_cos != 0 else (box_width_child if parent_sin < 0 else 0))
        parent_y = y2+(((box_height_parent if parent_cos != 0 else(box_height_parent/2)) if parent_cos <= 0 else 0) if parent_sin >= 0 else box_height_parent/2)
        print(f"parent {parent} angle:{self.classes[parent]["angle"]}, sin: {self.angle_radius_sin_optimized(self.classes[parent]["angle"])}, cos: {self.angle_radius_cos_optimized(self.classes[parent]["angle"])}, x: {x2}, y: {y2}, child {child} angle: {self.classes[child]["angle"]}, sin: {self.angle_radius_sin_optimized(self.classes[child]["angle"])}, cos: {self.angle_radius_cos_optimized(self.classes[child]["angle"])}, x: {x1}, y: {y1}")
        print(f"child x,y: {(child_x, child_y)}, box_width_child: {box_width_child}, box_height_child: {box_height_child}")
        print(f"parent x, y: {(parent_x, parent_y)}, box_width_parent: {box_width_parent}, box_height_parent: {box_height_parent}")
        arrow = FancyArrowPatch(
            #(x1 + box_width_child*self.angle_radius_cos_optimized(self.classes[child]["angle"]) +self.angle_radius_sin_optimized(self.classes[child]["angle"]), y1 + box_height_child*self.angle_radius_sin_optimized(self.classes[child]["angle"])+self.angle_radius_cos_optimized(self.classes[child]["angle"])),
            #(x2 + box_width_parent*self.angle_radius_cos_optimized(self.classes[parent]["angle"]) +self.angle_radius_sin_optimized(self.classes[parent]["angle"]), y2 + box_height_parent*self.angle_radius_sin_optimized(self.classes[parent]["angle"]) +self.angle_radius_cos_optimized(self.classes[parent]["angle"])),
            (child_x,child_y),
            (parent_x,parent_y),
            arrowstyle="-|>", mutation_scale=15,
            color="black", linewidth=1.2
        )
        self.axes.add_patch(arrow)
        # Cardinalidade básica
        self.axes.text((x1 + x2) / 2 + 0.2, (y1 + y2) / 2 + 0.2, "0..* ➝ 1", fontsize=8, color="gray")

    def larger_class_size_attributes_dict(self, classes):
        max_size = 0
        #class_greater = None
        for class_name, class_data in classes.items():
            if len(class_data["attrs"]) > max_size:
                max_size = len(class_data["attrs"])
                #class_greater = class_name
        return max_size
    
    def larger_string_size_list(self, attributes):
        max_size = 0
        for attribute in attributes:
            if len(attribute) > max_size:
                max_size = len(attribute)
        return max_size
    
    def calculate_greater_area(self, classes):
        max_size = 0
        for class_name, class_data in classes.items():
            width = max(max(self.larger_string_size_list(class_data["attrs"]), len(class_name)) * self.FONTSIZE * 0.0035, self.BOX_WIDTH_DEFAULT)
            height = max(len(class_data["attrs"]) * self.FONTSIZE * 0.02, self.BOX_HEIGHT_DEFAULT)
            area = width * height
            print(f"classname: {class_name}, width: {width}, height: {height}, area: {area}")
            if area > max_size:
                max_size = area
        return max_size
    
    # Desenha as classes
    def draw_classes(self):
        count = 0
        depth = self.calculate_greater_area(self.classes)*0.5
        position_left = 0
        position_right = self.SIDES
        continue_draw = True
        continue_flag = continue_draw
        print(f"depth (greater area): {depth}, self.total_length: {self.total_length}")
        
        while continue_draw:
            continue_draw = continue_flag
            print("TEST")
            subclasses = dict(list(self.classes.items())[position_left:position_right])
            self._draw_box_recursively(0, depth, subclasses, self.SIDES, self.BOX_WIDTH_DEFAULT, self.BOX_HEIGHT_DEFAULT)
            position_left = position_right
            position_right = self.SIDES * (count+1) * 2
            depth = depth**2
            if position_right > self.total_length:
                position_right = self.total_length
                continue_flag = False
            
        for child, parent in self.relationships:
             self._draw_relationship(child, parent, classes)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Definição das classes
    classes = {
        "FUNC_BENEFICIO_CAD": {
            "attrs": [
                "Cod_Beneficiosadkjhfgsdjhfgsdjhgfsjhdfgsjdhgfjshdgfshdgfjgsdjhfsdgfjhsgdjfgsdgfm: Int",
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

    controller = Controller(classes, relationships)
    controller.draw_classes()