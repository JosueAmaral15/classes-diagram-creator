# [] pegar os números 3,4,5,6,7 e 10 para fazer as operações de orientação de estrutura. Se o resto da divisão é as operações aritméticas não derem um desses números, então o default para a estrutura de montagem de um diagrama de classes é 4.

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines
from math import sin, cos, floor, pi, atan2, isinf
from tqdm import tqdm

class GraphicDrawing:
    
    def __init__(self, classes = None, relationships = None, sides = 4, limit_classes = float("inf"), limit_relationships = float("inf")):
        
        #constants
        self.BOX_WIDTH_DEFAULT, self.BOX_HEIGHT_DEFAULT = 1.6, 0.8
        self.FONTSIZETITLE = 10
        self.FONTSIZE = 8
        
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
        self.text = dict()
        self.text['title'] = list()
        self.text['data'] = list()
        
        #numbers
        self.limit_classes = limit_classes
        self.limit_relationships = limit_relationships
        self.sides = sides
        
        #Initialize instance variables
        count=0
        for classes_name, class_data in self.classes.items():
            class_data["width"] = max(max(self.larger_string_size_list(class_data["attrs"]) * self.FONTSIZE * 0.004, len(classes_name)* self.FONTSIZETITLE * 0.004), self.BOX_WIDTH_DEFAULT)
            class_data["height"] = max(self.BOX_HEIGHT_DEFAULT +len(class_data["attrs"]) * self.FONTSIZE * 0.025,self.BOX_HEIGHT_DEFAULT)
            class_data["angle"] = count*(360//self.sides)
            count+=1
        
        count=0
        count2 = 0
        depth = self.calculate_greater_area(self.classes)
        depth2 = depth
        for classes_name, class_data in self.classes.items():
            x,y = self.angle_radius_sin_optimized(class_data["angle"]+((180//self.sides) if (count//self.sides % 2) else 0))*depth, self.angle_radius_cos_optimized(class_data["angle"]+((180//self.sides) if (count//self.sides % 2) else 0))*depth
            class_data["pos"] = (x,y)
            print(f"depth: {depth} depth2: {depth2}")
            if (count+1) % self.sides*2 == 0:
                try:
                    count2+=2
                    depth = depth2*(count2+1)
                except:
                    pass
            count+=1
            
        self.total_length = len(self.classes)
        self.MAXIMUM = 100
        
        self.fig, self.axes = plt.subplots(figsize=(12, 6))
        self.base_xlim = self.axes.get_xlim()
        self.base_ylim = self.axes.get_ylim()
        self.axes.callbacks.connect("xlim_changed", self.update_text_fontsize)
        self.axes.callbacks.connect("ylim_changed", self.update_text_fontsize)
        self.axes.set_xlim(-3, 10)
        self.axes.set_ylim(-3, 8)
        self.axes.axis("on")
    
    def update_text_fontsize(self, event):
        # Obtém limites atuais do eixo
        cur_xlim = self.axes.get_xlim()
        cur_ylim = self.axes.get_ylim()

        # Calcula escala atual em relação aos limites base
        scale_x = abs((self.base_xlim[1] - self.base_xlim[0]) / (cur_xlim[1] - cur_xlim[0]))
        scale_y = abs((self.base_ylim[1] - self.base_ylim[0]) / (cur_ylim[1] - cur_ylim[0]))

        # Usa a menor escala para manter proporção visual
        scale = max(scale_x, scale_y)*8
        print(f"scale_x: {scale_x}, scale_y: {scale_y}, scale: {scale}")

        # Atualiza o tamanho da fonte
        for text_title in self.text['title']:
            text_title.set_fontsize(self.FONTSIZE * scale)
            print("T1")
            
        for text_data in self.text['data']:
            text_data.set_fontsize(self.FONTSIZETITLE * scale)
            print("T2")

        # Redesenha
        self.fig.canvas.draw_idle()
    
    def _draw_box(self, class_name, class_data, x, y, box_width, box_height, edge_color="black", face_color="#e6f2ff"):
        
        # Caixa da classe
        self.axes.add_patch(FancyBboxPatch(
            (x, y), box_width, box_height,
            boxstyle="round,pad=0.05", edgecolor=edge_color, facecolor=face_color
        ))

        #título    
        local_title_y = y + box_height - 0.2
        text_title = self.axes.text(x + 0.05, local_title_y, class_name, fontsize=self.FONTSIZETITLE, weight="bold", va="top")
        self.text['title'].append(text_title)
        #dados
        for i, attr in enumerate(class_data["attrs"]):
            text_data = self.axes.text(x + 0.05, y +box_height -0.5 - self.FONTSIZETITLE * 0.02 * i, attr, fontsize=self.FONTSIZE, va="top")
            self.text['data'].append(text_data)

    def _draw_box_recursively(self, count, subclasses, sides, box_width, box_height, edge_color="black", face_color="#e6f2ff"):
        if count != sides:
            subclass = dict(list(subclasses.items())[count:count+1])
            for class_name, class_data in subclass.items():
                self._draw_box(class_name, class_data, class_data["pos"][0], class_data["pos"][1], max(class_data["width"], box_width), max(class_data["height"], box_height), edge_color, face_color)
            self._draw_box_recursively(count +1, subclasses, sides, box_width, box_height, edge_color, face_color)
        else:
            return
        

    def _draw_relationship(self, child, parent, classes):
        # Desenha relacionamentos com setas da TABELA FILHA para a PAI
        x1, y1 = self.classes[child]["pos"]
        x2, y2 = self.classes[parent]["pos"]
        
        #print("line 88", child)
        box_width_child = classes[child]["width"]
        box_height_child = classes[child]["height"]
        box_width_parent = classes[parent]["width"]
        box_height_parent = classes[parent]["height"]
        
        center = dict()
        for element_type in ['child', 'parent']:
            center[element_type] = dict()
        
        center['child']['x'] = x1+box_width_child/2
        center['child']['y'] = y1+box_height_child/2
        center['parent']['x'] = x2+box_width_parent/2
        center['parent']['y'] = y2+box_height_parent/2
               
        angle = atan2(center['parent']['y']-center['child']['y'],center['parent']['x']-center['child']['x'])
        
        child_sin = sin(angle)
        child_cos = cos(angle)
        parent_sin = -sin(angle)
        parent_cos = -cos(angle)
        
        child_x = center['child']['x']+child_cos*box_width_child/2 
        child_y = center['child']['y']+child_sin*box_height_child/2
        parent_x = center['parent']['x']+parent_cos*box_width_parent/2
        parent_y = center['parent']['y']+parent_sin*box_height_parent/2
        
        #print(f"child {child} angle: {angle}, sin: {child_sin}, cos: {child_cos}, x: {x1}, y: {y1}\nchild x,y: {(child_x, child_y)}, box_width_child: {box_width_child}, box_height_child: {box_height_child}")
        #print(f"parent {parent} angle:{angle}, sin: {parent_sin}, cos: {parent_cos}, x: {x2}, y: {y2},\nparent x, y: {(parent_x, parent_y)}, box_width_parent: {box_width_parent}, box_height_parent: {box_height_parent}")
        
        arrow = FancyArrowPatch(
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
            area = (class_data["width"] + class_data["height"])/2
            #print(f"classname: {class_name}, width: {width}, height: {height}, area: {area}")
            if area > max_size:
                max_size = area
        return max_size
    
    # Desenha as classes
    def draw_classes(self): 
        pbar = tqdm(total=self.MAXIMUM, desc="Process for draw classes")
        count = 0
        position_left = 0
        position_right = self.sides
        continue_draw = True
        continue_flag = continue_draw
        incrementation = (self.sides/self.total_length)*self.MAXIMUM
        total_incrementation = 0
        if total_incrementation + incrementation > self.MAXIMUM:
            incrementation = self.MAXIMUM -total_incrementation
            if total_incrementation + incrementation > self.MAXIMUM:
                incrementation = 0
        
        total_incrementation += incrementation
        #print(f"DEBUG 181 incrementation: {incrementation}")
        pbar.update(incrementation)
        while continue_draw:
            #print("DEBUG 184",incrementation, total_incrementation, total_incrementation + incrementation)
            if total_incrementation + incrementation > self.MAXIMUM:
                incrementation = self.MAXIMUM -total_incrementation
                if total_incrementation + incrementation > self.MAXIMUM:
                    incrementation = 0
            
            total_incrementation += incrementation
            #print(f"total_incrementation: {total_incrementation}")
            pbar.update(incrementation)
            continue_draw = continue_flag
            
            if  self.limit_classes > count*self.sides:
                subclasses = dict(list(self.classes.items())[position_left:position_right])
                self._draw_box_recursively(0, subclasses, self.sides, self.BOX_WIDTH_DEFAULT, self.BOX_HEIGHT_DEFAULT)
                position_left = position_right
                position_right = self.sides * (count+1) * 2
                #print(f"position_right: {position_right}, self.total_length: {self.total_length}")
                count+=1
                if position_right >= self.total_length:
                    position_right = self.total_length
                    continue_flag = False
            else:
                incrementation = self.MAXIMUM -total_incrementation
                pbar.update(incrementation)
                break
        
        pbar = None
        pbar = tqdm(total=self.MAXIMUM, desc="Process for draw relationships")
        relationships_quantity = len(self.relationships)
        incrementation = (1/relationships_quantity)*self.MAXIMUM
        total_incrementation = 0
        if total_incrementation + incrementation > self.MAXIMUM:
            incrementation = self.MAXIMUM -total_incrementation
            if total_incrementation + incrementation > self.MAXIMUM:
                incrementation = 0
        total_incrementation += incrementation
        pbar.update(incrementation)
        
        count = 0
        for child, parent in self.relationships:
            #print("line 221", child)
            if total_incrementation + incrementation > self.MAXIMUM:
                incrementation = self.MAXIMUM -total_incrementation
                if total_incrementation + incrementation > self.MAXIMUM:
                    incrementation = 0
            total_incrementation += incrementation
            
            pbar.update(incrementation)
            if  self.limit_relationships > count:
                #print("line 229", child)
                self._draw_relationship(child, parent, classes)
            else:
                incrementation = self.MAXIMUM -total_incrementation
                pbar.update(incrementation)
                break
                
            count+=1
                
        plt.tight_layout()
        plt.show()
        
class Controller:
    
    @staticmethod
    def get_content():
        validated = False
        while not validated:
            try:
                name = input("Digite o nome do arquivo com o esquema: ")
                with open(name) as file:
                    content = file.read()
                validated = True
            except:
                print("Erro na tentativa de ler o arquivo. Tente novamente!")
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
    controller = None
    drawing = None
    if choice == '1':
        controller = Controller()
        content = controller.get_content()
        content = controller.get_scope_type(content, TYPE)
        classes = controller.convert_tables_to_JSON(content, TYPE)
        relationships = controller.identify_relationships(classes)
        drawing = GraphicDrawing(classes, relationships, sides = 4, limit_classes = 10, limit_relationships = 10)
    else:
        drawing = GraphicDrawing(classes, relationships)
        
    if drawing is not None:
        drawing.draw_classes()