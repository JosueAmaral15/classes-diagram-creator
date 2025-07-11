# [] pegar os números 3,4,5,6,7 e 10 para fazer as operações de orientação de estrutura. Se o resto da divisão é as operações aritméticas não derem um desses números, então o default para a estrutura de montagem de um diagrama de classes é 4.

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.widgets import RadioButtons
#import matplotlib.lines as mlines
from matplotlib.widgets import TextBox
from math import sin, cos, floor, pi, atan2, isinf
from tqdm import tqdm
from statistics import harmonic_mean, geometric_mean

PRINT_CLASS_NAMES = True

class GraphicDrawing:
    
    def __init__(self, classes = None, relationships = None, sides = 4, limit_classes = float("inf")):
        
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
        self.texts_found = list()
        
        #numbers
        self.limit_classes = limit_classes
        self.sides = sides
        self.totalTextElement = 0
        self.index_atual = 0
        
        #strings
        self.valor_buscado = str()
        
        #Initialize instance variables
        count=0
        self.greater_width = 0
        self.greater_height = 0
        if PRINT_CLASS_NAMES:
            print("\nFound following class names: ")
        for class_name, class_attributes in self.classes.items():
            class_attributes["width"] = max(max(self.larger_string_size_list(class_attributes["attrs"]) * self.FONTSIZE * 0.004, len(class_name)* self.FONTSIZETITLE * 0.004), self.BOX_WIDTH_DEFAULT)
            class_attributes["height"] = max(self.BOX_HEIGHT_DEFAULT +len(class_attributes["attrs"]) * self.FONTSIZE * 0.025,self.BOX_HEIGHT_DEFAULT)
            class_attributes["angle"] = count*(360//self.sides)
            count+=1
            self.text[class_name] = dict()
            self.text[class_name]['title_axes_text'] = None
            self.text[class_name]['attributes_axes_text'] = list()
            self.text[class_name]['title'] = class_name
            self.text[class_name]['attributes'] = class_attributes["attrs"]
            self.text[class_name]['width'] = class_attributes["width"]
            self.text[class_name]['height'] = class_attributes["height"]
            self.text[class_name]['box'] = None
            if PRINT_CLASS_NAMES:
                print(f"{class_name}")
            
            if class_attributes["width"] > self.greater_width:
                self.greater_width = class_attributes["width"]
            
            if class_attributes["height"] > self.greater_height:
                self.greater_height = class_attributes["height"]
                
        if PRINT_CLASS_NAMES:
            print("\n")
            
        self.total_length = len(self.classes)
        self.MAXIMUM = 100
        
        self.fig, self.axes = plt.subplots(figsize=(12, 6))
        self.fig.set_constrained_layout(True)
        axbox = self.fig.add_axes([0.2, 0.05, 0.6, 0.075])  # [left, bottom, width, height]
        self.text_box = TextBox(axbox, "Buscar texto:")
        self.text_box.on_submit(self.buscar_texto)
        axes_radio = plt.axes([0.05, 0.4, 0.2, 0.2])  # [left, bottom, width, height]
        self.radio = RadioButtons(axes_radio, ('Palavra exata', 'Palavra Aproximada'))
        self.radio.on_clicked(self.mudar_pesquisa)
        self.search_function = lambda a,b: a.lower() == b.lower()
        self.base_xlim = self.axes.get_xlim()
        self.base_ylim = self.axes.get_ylim()
        self.axes.callbacks.connect("xlim_changed", self.update_dimensions)
        self.axes.callbacks.connect("ylim_changed", self.update_dimensions)
        self.fig.canvas.mpl_connect("key_press_event", self.tratar_tecla)
        self.axes.set_xlim(-3, 10)
        self.axes.set_ylim(-3, 8)
        self.axes.axis("on")
    
    def mudar_pesquisa(self, label):
        if label == 'Palavra exata':
            self.search_function = lambda a,b: a.lower() == b.lower()
        elif label == 'Palavra Aproximada':
            self.search_function = lambda a, b: a.lower() in b.lower()
        
        if self.valor_buscado:
            self._focar_indice()
    
    # Callback de busca
    def buscar_texto(self, valor):
        self.texts_found = list()
        self.totalTextElement = 0
        self.valor_buscado = valor.strip().lower()
        found = False
        for class_name in self.classes.keys():
            for text in self.text[class_name]['attributes_axes_text']+[self.text[class_name]['title_axes_text']]:
                if self.search_function(self.valor_buscado, text.get_text()):
                    self.texts_found.append(text)
                    if not found:
                        found = True
        if found:
            self.totalTextElement = len(self.texts_found)
            x, y = text.get_position()
            w, h = 5, 5
            self.axes.set_xlim(x - w/2, x + w/2)
            self.axes.set_ylim(y - h/2, y + h/2)
            self.fig.canvas.draw_idle()
        else:
            print("Texto não encontrado:", self.valor_buscado)
    
    def tratar_tecla(self, event):
        #print(f"self.texts_found: {self.texts_found}, self.totalTextElement: {self.totalTextElement}")
        if event.key == "pageup":
            self.index_atual = (self.index_atual - 1) % self.totalTextElement
            self._focar_indice()
        elif event.key == "pagedown" or event.key == "enter":
            self.index_atual = (self.index_atual + 1) % self.totalTextElement
            self._focar_indice()
        elif event.key == "esc":
            self.text_box.set_val("")  # Limpa o campo
            self.texts_found[self.index_atual].set_color("black")
            self.fig.canvas.draw_idle()

    def _focar_indice(self):
        for text in self.texts_found:
            text.set_color("black")
        texto = self.texts_found[self.index_atual]
        texto.set_color("red")
        x, y = texto.get_position()
        self.axes.set_xlim(x - 3, x + 3)
        self.axes.set_ylim(y - 3, y + 3)
        #self.text_box.set_val(texto.get_text())
        self.fig.canvas.draw_idle()
    
    def update_dimensions(self, event):
        self.update_text_fontsize()


    def calculate_scale(self):
        # Obtém limites atuais do eixo
        cur_xlim = self.axes.get_xlim()
        cur_ylim = self.axes.get_ylim()

        # Calcula escala atual em relação aos limites base
        scale_x = abs((self.base_xlim[1] - self.base_xlim[0]) / (cur_xlim[1] - cur_xlim[0]))
        scale_y = abs((self.base_ylim[1] - self.base_ylim[0]) / (cur_ylim[1] - cur_ylim[0]))

        # Usa a menor escala para manter proporção visual
        scale = max(scale_x, scale_y)
        
        return scale
    
    def update_text_fontsize(self):
        scale = self.calculate_scale()
        #print(f"scale_x: {scale_x}, scale_y: {scale_y}, scale: {scale}")
        
        # Atualiza o tamanho da fonte
        for text in self.text.values():
            #text['title_axes_text'].set_fontsize(self.FONTSIZE * scale)
            if text is not None:
                area_factor = 10 #(text['width']* text['height'])
                if text['title_axes_text'] is not None:
                    #print(text['width'])
                    #print(f"self.FONTSIZETITLE: {self.FONTSIZETITLE}, area_factor: {area_factor}, scale: {scale}")
                    fontsizetitle = min(max(self.FONTSIZETITLE * area_factor * scale, 1), 26)
                    text['title_axes_text'].set_fontsize(fontsizetitle)
                if text['attributes_axes_text'] is not None:
                    for text_attributes in text['attributes_axes_text']:
                        #text_attributes.set_fontsize(self.FONTSIZETITLE * scale)
                        if text_attributes is not None:
                            fontsizeattribute = min(self.FONTSIZE * area_factor * scale, 24)
                            text_attributes.set_fontsize(fontsizeattribute)
        # Redesenha
        self.fig.canvas.draw_idle()
    
    def _draw_box(self, class_name, class_attributes, x, y, box_width, box_height, edge_color="black", face_color="#e6f2ff"):
        
        # Caixa da classe
        self.text[class_name]['box'] = FancyBboxPatch(
            (x, y), box_width, box_height,
            boxstyle="round,pad=0.05", edgecolor=edge_color, facecolor=face_color
        )
        
        self.axes.add_patch(self.text[class_name]['box'])

        #título    
        local_title_y = y + box_height - 0.2
        text_title = self.axes.text(x + 0.05, local_title_y, class_name, fontsize=self.FONTSIZETITLE, weight="bold", va="top")
        self.text[class_name]['title_axes_text'] = text_title
        
        #dados
        for i, attr in enumerate(class_attributes["attrs"]):
            text_attributes = self.axes.text(x + 0.05, y +box_height -0.5 - self.FONTSIZETITLE * 0.02 * i, attr, fontsize=self.FONTSIZE, va="top")
            self.text[class_name]['attributes_axes_text'].append(text_attributes)

    def _draw_box_recursively(self, count, subclasses, sides, box_width, box_height, edge_color="black", face_color="#e6f2ff"):
        if count != sides:
            subclass = dict(list(subclasses.items())[count:count+1])
            for class_name, class_attributes in subclass.items():
                self._draw_box(class_name, class_attributes, class_attributes["pos"][0], class_attributes["pos"][1], max(class_attributes["width"], box_width), max(class_attributes["height"], box_height), edge_color, face_color)
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
        for class_name, class_attributes in classes.items():
            if len(class_attributes["attrs"]) > max_size:
                max_size = len(class_attributes["attrs"])
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
        for class_name, class_attributes in classes.items():
            area = (class_attributes["width"] + class_attributes["height"])/2
            #print(f"classname: {class_name}, width: {width}, height: {height}, area: {area}")
            if area > max_size:
                max_size = area
        return max_size
    
    # Desenha as classes
    def draw_classes(self): 
        pbar = tqdm(total=self.MAXIMUM, desc="Process for draw classes")
        count = 0
        count2 = 0
        position_left = 0
        continue_draw = True
        classes_drawed = list()
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
            
            if  self.limit_classes > count*self.sides:
                position_right = self.sides * (count+1)
                if position_right > self.limit_classes:
                    position_right = self.limit_classes
                #print(f"position_left: {position_left},  position_right: {position_right}")
                #print(f"self.limit_classes: {self.limit_classes}, count*self.sides: {count*self.sides}: self.limit_classes > count*self.sides: {self.limit_classes > count*self.sides}")
                subclasses = dict(list(self.classes.items())[position_left:position_right])
                
                depth = self.calculate_greater_area(subclasses) *(count2+1)
                count2+= 2
                #print(f"count: {count}")
                for class_name, class_attributes in subclasses.items():
                    x,y = self.angle_radius_sin_optimized(class_attributes["angle"]+((180//self.sides) if (count % 2) else 0))*depth, self.angle_radius_cos_optimized(class_attributes["angle"]+((180//self.sides) if (count % 2) else 0))*depth
                    class_attributes["pos"] = (x,y)
                    
                #print(f"before: classes_drawed: {classes_drawed}, len(classes_drawed): {len(classes_drawed)}")
                classes_drawed += list(self.classes.keys())[position_left:position_right]
                #print(f"after: classes_drawed: {classes_drawed}, len(classes_drawed): {len(classes_drawed)}")
                self._draw_box_recursively(0, subclasses, self.sides, self.BOX_WIDTH_DEFAULT, self.BOX_HEIGHT_DEFAULT)
                position_left = position_right
                #print(f"self.sides: {self.sides}, count: {count}, self.sides * (count+1) * 2: {self.sides * (count+1) * 2}")
                #print(f"after position_right: {position_right}")
                #print(f"position_right: {position_right}, self.total_length: {self.total_length}")
                count+=1
                if position_right >= self.total_length:
                    position_right = self.total_length
                    continue_draw = False
            else:
                continue_draw = False

        incrementation = self.MAXIMUM -total_incrementation
        pbar.update(incrementation)
        
        #print(f"self.limit_classes: {self.limit_classes}, count*self.sides: {count*self.sides}, len(classes_drawed): {len(classes_drawed)} classes_drawed: {classes_drawed}")
        
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
        
        #print(f"classes_drawed: {classes_drawed}")
        for child, parent in self.relationships:
            #print("line 221", child)
            if total_incrementation + incrementation > self.MAXIMUM:
                incrementation = self.MAXIMUM -total_incrementation
                if total_incrementation + incrementation > self.MAXIMUM:
                    incrementation = 0
            total_incrementation += incrementation
            
            pbar.update(incrementation)
            if list(filter(lambda x: child == x, classes_drawed)) and list(filter(lambda x: parent == x, classes_drawed)):
                #print(f"line 263, child: {child}, parent: {parent}")
                self._draw_relationship(child, parent, classes)
                
        incrementation = self.MAXIMUM -total_incrementation
        pbar.update(incrementation)
        
        ##self.totalTextElement = len(self.text[class_name]['attributes_axes_text']+[self.text[class_name]['title_axes_text']])
                
        plt.tight_layout()
        plt.show()
        
class Controller:
    
    @staticmethod
    def get_content():
        validated = False
        while not validated:
            try:
                name = input("Enter the file name with the squema: ")
                with open(name) as file:
                    content = file.read()
                validated = True
            except:
                print("Error while reading the file. Try again!")
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
        choice = input("Do you want to limit the scope of the classes? (y/n): ")
        
        if choice.lower() == 'y':
            quantity = 'error'
            while not quantity.isdigit():
                quantity = input("Define a integer limit quantity: ")
            quantity = int(quantity)
            choice = input("Would you like to enter the sides quantity (y/n): ")
            sides_quantity = 'error'
            if choice.lower() == 'y':
                while not sides_quantity.isdigit():
                    sides_quantity = input("Enter the sides quantity: ")
                sides_quantity = int(sides_quantity)
                drawing = GraphicDrawing(classes, relationships, sides = sides_quantity, limit_classes = quantity)
            else:
                drawing = GraphicDrawing(classes, relationships, sides = 4, limit_classes = quantity)
        else:
            choice = input("Would you like to enter the sides quantity (y/n): ")
            sides_quantity = 'error'
            if choice.lower() == 'y':
                while not sides_quantity.isdigit():
                    sides_quantity = input("Enter the sides quantity: ")
                sides_quantity = int(sides_quantity)
                drawing = GraphicDrawing(classes, relationships, sides = sides_quantity)
            else:
                drawing = GraphicDrawing(classes, relationships)
    else:
        drawing = GraphicDrawing(classes, relationships)
        
    if drawing is not None:
        drawing.draw_classes()