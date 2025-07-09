# [] pegar os números 3,4,5,6,7 e 10 para fazer as operações de orientação de estrutura. Se o resto da divisão é as operações aritméticas não derem um desses números, então o default para a estrutura de montagem de um diagrama de classes é 4.

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines
from math import sin, cos, floor, pi, atan2, isinf
from tqdm import tqdm

class Controller:
    def __init__(self, classes, relationships, limit_classes = float("inf"), limit_relationships = float("inf")):
        
        #constants
        self.BOX_WIDTH_DEFAULT, self.BOX_HEIGHT_DEFAULT = 1.6, 0.8
        self.FONTSIZE = 10
        self.SIDES = 4
        self.CENTROID = {'x': 1, 'y': 1}
        #functions
        self.precision_function = lambda x, expoent: x * floor(0.5 * (abs(x - 10**(-expoent) + 1) - abs(x - 10**(-expoent)) + 1)) - x * floor(0.5 * (abs(x + 10**(-expoent) + 1) - abs(x + 10**(-expoent)) + 1)) + x
        self.angle_radius_sin = lambda x : sin(pi*x/180)
        self.angle_radius_sin_optimized = lambda x: self.precision_function(self.angle_radius_sin(x), 6)
        self.angle_radius_cos = lambda x : cos(pi*x/180)
        self.angle_radius_cos_optimized = lambda x: self.precision_function(self.angle_radius_cos(x), 6)
                
        #objects
        self.classes = classes
        self.relationships = relationships
        self.pbar = None
        
        #numbers
        self.total_length = len(self.classes)
        self.limit_classes = limit_classes
        self.limit_relationships = limit_relationships
        
        for classes_name in self.classes.keys():
            self.classes[classes_name]["width"] = self.BOX_WIDTH_DEFAULT
            self.classes[classes_name]["height"] = self.BOX_HEIGHT_DEFAULT
            self.classes[classes_name]["angle"] = 0
            self.classes[classes_name]["pos"] = (0,0)
        
        fig, self.axes = plt.subplots(figsize=(12, 6))
        self.axes.set_xlim(-3, 10)
        self.axes.set_ylim(-3, 8)
        self.axes.axis("on")

    def _draw_box(self, class_name, class_data, x, y, box_width, box_height, edge_color="black", face_color="#e6f2ff"):
        #print("TESTE2342")
        class_data["pos"] = (x,y)
        if box_height +len(class_data["attrs"]) * self.FONTSIZE * 0.02 > box_height:
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
        
        print(child)
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
        
        # center = dict()
        # for element_type in ['child', 'parent']:
        #     center[element_type] = dict()
        
        # center['child']['x'] = x1/2
        # center['child']['y'] = y1/2
        # center['parent']['x'] = x2/2
        # center['parent']['y'] = y2/2
        
        # angle = atan2(center['parent']['x']-center['child']['x'],center['parent']['y']-center['child']['y'])
        
        #child_x = x1+
        #child_y = y1+
        #parent_x = x2+
        #parent_y = y2+
        
        #print(f"parent {parent} angle:{self.classes[parent]["angle"]}, sin: {self.angle_radius_sin_optimized(self.classes[parent]["angle"])}, cos: {self.angle_radius_cos_optimized(self.classes[parent]["angle"])}, x: {x2}, y: {y2}, child {child} angle: {self.classes[child]["angle"]}, sin: {self.angle_radius_sin_optimized(self.classes[child]["angle"])}, cos: {self.angle_radius_cos_optimized(self.classes[child]["angle"])}, x: {x1}, y: {y1}")
        #print(f"child x,y: {(child_x, child_y)}, box_width_child: {box_width_child}, box_height_child: {box_height_child}")
        #print(f"parent x, y: {(parent_x, parent_y)}, box_width_parent: {box_width_parent}, box_height_parent: {box_height_parent}")
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
            #print(f"classname: {class_name}, width: {width}, height: {height}, area: {area}")
            if area > max_size:
                max_size = area
        return max_size
    
    # Desenha as classes
    def draw_classes(self):
        MAXIMUM = 100
        pbar = tqdm(total=MAXIMUM, desc="Process for draw classes")
        count = 0
        depth = self.calculate_greater_area(self.classes)*0.5
        position_left = 0
        position_right = self.SIDES
        continue_draw = True
        continue_flag = continue_draw
        #print(f"depth (greater area): {depth}, self.total_length: {self.total_length}")
        incrementation = (self.SIDES/self.total_length)*MAXIMUM
        total_incrementation = 0
        if total_incrementation + incrementation > MAXIMUM:
            incrementation = MAXIMUM -total_incrementation
            if total_incrementation + incrementation > MAXIMUM:
                incrementation = 0
        
        total_incrementation += incrementation
        #print(f"DEBUG 181 incrementation: {incrementation}")
        pbar.update(incrementation)
        while continue_draw:
            #print("DEBUG 184",incrementation, total_incrementation, total_incrementation + incrementation)
            if total_incrementation + incrementation > MAXIMUM:
                incrementation = MAXIMUM -total_incrementation
                if total_incrementation + incrementation > MAXIMUM:
                    incrementation = 0
            
            total_incrementation += incrementation
            #print(f"total_incrementation: {total_incrementation}")
            pbar.update(incrementation)
            continue_draw = continue_flag
            
            if  self.limit_classes > count*self.SIDES:
                subclasses = dict(list(self.classes.items())[position_left:position_right])
                self._draw_box_recursively(0, depth, subclasses, self.SIDES, self.BOX_WIDTH_DEFAULT, self.BOX_HEIGHT_DEFAULT)
                position_left = position_right
                position_right = self.SIDES * (count+1) * 2
                #print(f"position_right: {position_right}, self.total_length: {self.total_length}")
                count+=1
                try:
                    depth = depth**2
                except:
                    pass
                if position_right >= self.total_length:
                    position_right = self.total_length
                    continue_flag = False
            else:
                incrementation = MAXIMUM -total_incrementation
                pbar.update(incrementation)
                break
        
        pbar = None
        pbar = tqdm(total=MAXIMUM, desc="Process for draw relationships")
        relationships_quantity = len(self.relationships)
        incrementation = (1/relationships_quantity)*MAXIMUM
        total_incrementation = 0
        if total_incrementation + incrementation > MAXIMUM:
            incrementation = MAXIMUM -total_incrementation
            if total_incrementation + incrementation > MAXIMUM:
                incrementation = 0
        total_incrementation += incrementation
        pbar.update(incrementation)
        
        count = 0
        for child, parent in self.relationships:
            if total_incrementation + incrementation > MAXIMUM:
                incrementation = MAXIMUM -total_incrementation
                if total_incrementation + incrementation > MAXIMUM:
                    incrementation = 0
            total_incrementation += incrementation
            
            pbar.update(incrementation)
            if  self.limit_relationships > count:
                self._draw_relationship(child, parent, classes)
            else:
                incrementation = MAXIMUM -total_incrementation
                pbar.update(incrementation)
                break
                
            count+=1
                
        plt.tight_layout()
        plt.show()

    @staticmethod
    def get_content():
        name = input("Digite o nome do arquivo com o esquema: ")
        with open(name) as file:
            content = file.read()
        return content

    @staticmethod
    def get_scope_type(content, type):
        ENTER = '\n'
        content_lines = content.split(ENTER)
        reading = False
        result = str()
        for line in content_lines:
            if type in line and "{" in line:
                reading = True
            elif "}" in line:
                if reading:
                    result+='}'+ENTER
                    reading = False
            
            if reading:
                result+=line+ENTER
        
        return result

    @staticmethod
    def convert_tables_to_JSON(content, type):
        ENTER = '\n'
        content_lines = content.split(ENTER)
        classes = dict()
        reading = False
        first = True
        for line in content_lines:
            if '{' in line:
                classe = dict()
                attrs = list()
                reading = True
                first = True
                name = line.replace(type, "").replace("{","").strip()
            
            if '}' in line:
                classe['attrs'] = attrs
                classes[name] = classe
                reading = False

            if reading:
                if not first:
                    if line and not '//' in line:
                        attrs.append(line)
                else:
                    first = False
        return classes

    @staticmethod
    def identify_relationships(classes):
        relationships = set()
        for name1, attrs1 in classes.items():
            for name2, attrs2 in classes.items():
                if name1 != name2:
                    for name_attr, content_attr in attrs2.items():
                        for attr in content_attr:
                            if name1.strip() in attr:
                                relationships.add((name1, name2))
        return list(relationships)

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

    TYPE = 'model'
    choice = input("Class Diagram Creator\n\nChoose an option:\n\n\t1.Create my own class diagram.\n\t2. Create a example.\n\noption: ")
    controller = Controller(classes, relationships, limit_classes = 10, limit_relationships = 10)
    if choice == '1':
        content = controller.get_content()
        content = controller.get_scope_type(content, TYPE)
        classes = controller.convert_tables_to_JSON(content, TYPE)
        relationships = controller.identify_relationships(classes)
    controller.draw_classes()