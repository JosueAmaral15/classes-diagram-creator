# [] pegar os números 3,4,5,6,7 e 10 para fazer as operações de orientação de estrutura. Se o resto da divisão é as operações aritméticas não derem um desses números, então o default para a estrutura de montagem de um diagrama de classes é 4.
import sys
from threading import Thread
from flask import Flask
import dash
from dash import html, dcc, Output, Input, State
import dash_cytoscape as cyto
from dash.dependencies import ClientsideFunction
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from dash_iconify import DashIconify
from math import sin, cos, floor, pi, atan2, isinf
from tqdm import tqdm
from statistics import harmonic_mean, geometric_mean

PRINT_CLASS_NAMES = True

class GraphicDrawing:
    
    def __init__(self, classes = None, relationships = None, sides = 4, limit_classes = float("inf")):
        
        #constants
        self.BOX_WIDTH_DEFAULT, self.BOX_HEIGHT_DEFAULT = 160, 80
        self.FONTSIZETITLE = 10
        self.FONTSIZE = 8
        
        #booleans
        self.is_selected_text = False
        self.is_selected_text_wrapper = False
        
        #functions
        self.precision_function = lambda x, expoent: x * floor(0.5 * (abs(x - 10**(-expoent) + 1) - abs(x - 10**(-expoent)) + 1)) - x * floor(0.5 * (abs(x + 10**(-expoent) + 1) - abs(x + 10**(-expoent)) + 1)) + x
        self.angle_radius_sin = lambda x : sin(pi*x/180)
        self.angle_radius_sin_optimized = lambda x: self.precision_function(self.angle_radius_sin(x), 6)
        self.angle_radius_cos = lambda x : cos(pi*x/180)
        self.angle_radius_cos_optimized = lambda x: self.precision_function(self.angle_radius_cos(x), 6)
                
        #objects
        self.classes = classes if limit_classes == float("inf") else classes[:limit_classes]
        self.elements = list()
        self.pbar = None
        self.previous_text = None
        self.relationships = relationships
        self.text = dict()
        self.texts_found = list()
        
        #numbers
        self.fim_texto_cursor = 0
        self.index_atual = 0
        self.inicio_texto_cursor = 0
        self.limit_classes = limit_classes
        self.previous_text_box_search_length = 0
        self.sides = sides
        self.totalTextElement = 0
        self.growth_factor = 2
        
        #strings
        self.valor_buscado = str()
        self.previous_text_box_search = str()
        
        #Initialize instance variables
        count=0
        self.greater_width = 0
        self.greater_height = 0
        if PRINT_CLASS_NAMES:
            print("\nFound following class names: ")
        for class_name, class_attributes in self.classes.items():
            class_attributes["width"] = max(max(self.larger_string_size_list(class_attributes["attrs"]) * self.FONTSIZE*0.5, len(class_name)* self.FONTSIZETITLE), self.BOX_WIDTH_DEFAULT)
            class_attributes["height"] = max(self.BOX_HEIGHT_DEFAULT +len(class_attributes["attrs"]) * self.FONTSIZE,self.BOX_HEIGHT_DEFAULT)
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
            print(f"Total: {count} classes.\n")
            
        self.total_length = len(self.classes)
        self.MAXIMUM = 100
    
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
            #self.axes.set_xlim(x - w/2, x + w/2)
            #self.axes.set_ylim(y - h/2, y + h/2)
            ##self.fig.canvas.draw_idle()
        # else:
        #     print("Texto não encontrado:", self.valor_buscado)
    
    def tratar_tecla(self, event):
        #print(f"event.key == 'home' and event.shift: {event.key == 'shift+home'}, event.key == 'end' and event.shift: {event.key == 'shift+end'}")
        #print(f"self.texts_found: {self.texts_found}, self.totalTextElement: {self.totalTextElement}")
        self.text_box.set_val(str(self.text_box.text).replace("[", "").replace("]", ""))
        
        if event.key == "pageup":
            if self.totalTextElement > 0:
                self.index_atual = (self.index_atual - 1) % self.totalTextElement
                self._focar_indice()
        elif event.key == "pagedown" or event.key == "enter":
            if self.totalTextElement > 0:
                self.index_atual = (self.index_atual + 1) % self.totalTextElement
                self._focar_indice()
        elif event.key == "esc":
            if len(self.texts_found) > 0:
                self.text_box.set_val("")  # Limpa o campo
                self.texts_found[self.index_atual].set_color("black")
                self.cursor = 0
                #self.fig.canvas.draw_idle()
        elif event.key == 'shift+home':
            #print(f"DEBUG 148 tratar_tecla() <before> | cursor: {self.cursor}, self.text_box.text: {self.text_box.text}, len(self.text_box.text): {len(self.text_box.text)}, self.selecao_final: {self.selecao_final}, self.cursor: {self.cursor}")
            self.cursor = max(0, self.cursor)
            self.selecao_final = 0 #len(self.text_box.text)-1
            #print(f"DEBUG 150 tratar_tecla() <after> | cursor: {self.cursor}, self.text_box.text: {self.text_box.text}, len(self.text_box.text): {len(self.text_box.text)}, self.selecao_final: {self.selecao_final}, self.cursor: {self.cursor}")
            if abs(self.cursor -self.selecao_final) > 0:
                self.atualizar_texto_selecionado()
        elif event.key == 'shift+end':
            #print(f"DEBUG 153 tratar_tecla() <before> | cursor: {self.cursor}, self.text_box.text: {self.text_box.text}, len(self.text_box.text): {len(self.text_box.text)}, self.selecao_final: {self.selecao_final}, self.cursor: {self.cursor}")
            self.selecao_final = len(self.text_box.text) #max(self.cursor, self.selecao_final)
            self.cursor = min(len(self.text_box.text), self.cursor)
            #print(f"DEBUG 155 tratar_tecla() <after> | cursor: {self.cursor}, self.text_box.text: {self.text_box.text}, len(self.text_box.text): {len(self.text_box.text)}, self.selecao_final: {self.selecao_final}, self.cursor: {self.cursor}")
            if abs(self.cursor -self.selecao_final) > 0:
                self.atualizar_texto_selecionado()
        elif event.key == "left":
            self.cursor = max(0, self.cursor - 1)
        elif event.key == "right":
            self.cursor = min(len(self.text_box.text), self.cursor + 1)
        elif event.key == "end":
            self.cursor = len(self.text_box.text)
            self.selecao_final = 0
        elif event.key == "home":
            self.cursor = 0
            self.selecao_final = len(self.text_box.text)
        elif event.key == "delete" and self.is_selected_text:
            self.text_box.set_val(self.text_box.text.replace(self.text_box.text[self.inicio_texto_cursor:self.fim_texto_cursor], ""))
        elif event.key == "ctrl+a":
            self.cursor = 0
            self.selecao_final = len(self.text_box.text)
            self.atualizar_texto_selecionado()
        else:
            if self.previous_text_box_search_length < len(self.text_box.text):
                if self.previous_text_box_search == self.text_box.text[:-1]:
                    self.cursor+=1
                else:
                    self.search_cursor()
            self.previous_text_box_search = self.text_box.text
            self.previous_text_box_search_length = len(self.text_box.text)
        
        if not self.is_selected_text_wrapper:
            if self.is_selected_text:
                self.is_selected_text = False
        else:
            self.is_selected_text_wrapper = False
        
    def search_cursor(self):
        position = self.text_box.text.find(self.text_box.text[self.cursor:])+1
        if position != 0:
            self.cursor = position #+ self.cursor
            
    
    def atualizar_texto_selecionado(self):
        print(f"DEBUG 188 atualizar_texto_selecionado() | self.selecao_final: {self.selecao_final}, self.cursor: {self.cursor}")
        self.inicio_texto_cursor = min(self.cursor, self.selecao_final)
        self.fim_texto_cursor = max(self.cursor, self.selecao_final)
        selecionado = self.text_box.text[self.inicio_texto_cursor:self.fim_texto_cursor]
        print(f"DEBUG 162 atualizar_texto_selecionado()  | selecionado: {selecionado}")
        texto_visual = (self.text_box.text[:self.inicio_texto_cursor] +
                        "[" + selecionado + "]" +
                        self.text_box.text[self.fim_texto_cursor:])
        self.text_box.set_val(texto_visual)
        self.is_selected_text = True
        self.is_selected_text_wrapper = True
    
    def _focar_indice(self):
        if self.previous_text is not None:
            self.previous_text.set_color("black")
        texto = self.texts_found[self.index_atual]
        self.previous_text = texto
        texto.set_color("red")
        x, y = texto.get_position()
        #self.axes.set_xlim(x - 3, x + 3)
        #self.axes.set_ylim(y - 3, y + 3)
        #self.text_box.set_val(texto.get_text())
        #self.fig.canvas.draw_idle()
    
    def update_dimensions(self, event):
        self.update_text_fontsize()
    
    def _draw_box(self, class_name, class_attributes, x, y, box_width, box_height, edge_color="black", face_color="#e6f2ff"):
        
        # Caixa da classe
        attr_string = "\n".join(class_attributes["attrs"])
        element = {
            'data': {
                'id': class_name,
                'label': f"{class_name}\n\n{attr_string}" if attr_string else class_name,
            },
            'position': {
                'x': x,
                'y': y
            },
            'classes': 'classe',
            'style': {
                'background-color': face_color,     # fundo do nó (node)
                'border-color': edge_color,         # cor da borda (edge-color em nós)
                'font-size': self.FONTSIZE,
                'height': box_height,
                'width': box_width
            }
            
        }
        
        self.elements.append(element)

    def _draw_box_recursively(self, count, subclasses, sides, box_width, box_height, edge_color="black", face_color="#e6f2ff"):
        if count != sides:
            subclass = dict(list(subclasses.items())[count:count+1])
            for class_name, class_attributes in subclass.items():
                self._draw_box(class_name, class_attributes, class_attributes["pos"][0], class_attributes["pos"][1], max(class_attributes["width"], box_width), max(class_attributes["height"], box_height), edge_color, face_color)
            self._draw_box_recursively(count +1, subclasses, sides, box_width, box_height, edge_color, face_color)
        else:
            return

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
            area = (class_attributes["width"] +class_attributes["height"])/2
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
                    x,y = self.angle_radius_sin_optimized(class_attributes["angle"]+((180//self.sides) if (count % 2) else 0))*depth*(2 if (count % 2) else 1), self.angle_radius_cos_optimized(class_attributes["angle"]+((180//self.sides) if (count % 2) else 0))*depth
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
                self.elements.append({
                    'data': {
                        'source': child,
                        'target': parent,
                        'label': "0..* ➝ 1",
                    },
                    'classes': 'relacionamento',
                })
                
        incrementation = self.MAXIMUM -total_incrementation
        pbar.update(incrementation)
        
        return self.elements
        
class Controller:
    
    def __init__(self, type):
        self.type = type
        self.classes = None
        self.relationships = None
    
    @staticmethod
    def get_content():
        validated = False
        content = None
        while not validated:
            try:
                name = input("Enter the file name with the squema: ")
                if len(name) > 0:
                    with open(name) as file:
                        content = file.read()
                    validated = True
                else:
                    break
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

    # Thread para rodar o servidor Flask
    @staticmethod
    def run_server():
        server.run(debug=False, port=8050, use_reloader=False)
    
    def get_graphic_drawing_object(self):
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
            "FUNC_DEP": {
                "attrs": [],
                "pos": (3.2, 2)
            },
            "FUNC_CAD_EST_CIVIL": {
                "attrs": [
                    "Cod_Est_civil: Int",
                    "Estado_Civil: String?"
                ],
                "pos": (3, 1)
            },
            "FUNC_BENEFICIO": {
                "attrs": [],
                "pos": (0, 3)
            },
            "FUNC_CAD_EMPREGO": {
                "attrs": [
                    "Cod_Tipo_emprego: Int",
                    "Tipo_emprego: String"
                ],
                "pos": (1, 0)
            },
            "FUNC": {
                "attrs": [],
                "pos": (2, 0.8)
            }
        }

        # Relacionamentos
        relationships = [
            ("FUNC", "FUNC_CAD_EMPREGO"),
            ("FUNC", "FUNC_CAD_EST_CIVIL"),
            ("FUNC_DEP", "FUNC_CAD_EST_CIVIL"),
            ("FUNC_BENEFICIO", "FUNC_BENEFICIO_CAD"),
        ]
        choice = input("Class Diagram Creator\n\nChoose an option:\n\n\t1.Create my own class diagram.\n\t2. Create a example.\n\noption: ")
        drawing = None
        
        if choice == '1':
            content = controller.get_content()
            if content is not None:
                content = controller.get_scope_type(content, self.type)
                classes = controller.convert_tables_to_JSON(content, self.type)
                relationships = controller.identify_relationships(classes)
                choice = input("Do you want to limit the scope of the classes? (y/n): ")
                
                if choice.lower() == 'y':
                    quantity = 'error'
                    while not quantity.isdigit() or len(quantity) == 0:
                        quantity = input("Define a integer limit quantity: ")
                    if len(quantity) != 0:
                        quantity = int(quantity)
                        choice = input("Would you like to enter the sides quantity (y/n): ")
                        sides_quantity = 'error'
                        if choice.lower() == 'y':
                            while not sides_quantity.isdigit() or sides_quantity == '':
                                sides_quantity = input("Enter the sides quantity: ")
                            
                            if sides_quantity != '':
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
        
        self.classes = classes
        self.relationships = relationships
        return drawing

# Janela Qt
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualização de Classes com Cytoscape")
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 800
        self.resize(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.center_x = 0
        self.center_y = 0
        self.current_x = 0
        self.current_y = 0
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://localhost:8050/cytoscape/"))
        self.browser.loadFinished.connect(self.on_load_finished)
        self.setCentralWidget(self.browser)
        
    def on_load_finished(self):
        js_disable_scroll = """
            document.body.style.overflow = 'hidden';
            document.documentElement.style.overflow = 'hidden';
        """
        self.browser.page().runJavaScript(js_disable_scroll)
    
if __name__ == "__main__":
    
    TYPE = 'model'
    # Flask + Dash
    server = Flask(__name__)
    dash_app = dash.Dash(__name__, server=server, url_base_pathname='/cytoscape/')
    
    controller = Controller(type = TYPE)
    drawing = controller.get_graphic_drawing_object()
        
    if drawing is not None:
        elements = drawing.draw_classes()
        
        stylesheet = [{
            'selector': '.relacionamento',
            'style': {
                'curve-style': 'bezier',
                'font-size': 10,
                'label': 'data(label)',
                'line-color': 'black',
                'target-arrow-shape': 'triangle',
                'target-arrow-color': 'black',
                'text-background-color': '#ffffff',
                'text-background-opacity': 1,
                'text-margin-y': -10,
                'text-rotation': 'autorotate',
                'width': 1.5,
                }
        }, {
                'selector': '.classe',
                'style': {
                    'border-width': 1,
                    'color': '#003366',
                    'text-justification': 'left',
                    'label': 'data(label)',
                    'padding': '5px',
                    'shape': 'roundrectangle',
                    'text-halign': 'center',
                    'text-valign': 'center',
                    'text-wrap': 'wrap',
                }
        },
        {
            'selector': '.invisible',
            'style': {
                'background-opacity': 0,
                'border-opacity': 0,
                'label': '',
                'width': 1,
                'height': 1
            }
        },
        {
            'selector': '.highlight',
            'style': {
                'background-color': '#ffff00',
                'text-background-color': '#ffff00',
                'text-background-opacity': 1,
                'border-width': 3,
                'border-color': 'orange',
                'target-arrow-color': 'yellow',
                'transition-property': 'background-color, line-color, target-arrow-color',
                'transition-duration': '0.5s'
            }
        }
        ]
        
        for element in elements: # Remover a classe style do dicionário dos elementos e passar para o stylesheet a fim de não dar avisos desnecessários e nem inconsistências.
            if 'data' in element:
                if 'id' in element['data']:
                    id = element['data']['id']
                    if 'style' in element:
                        style = element['style']
                        new_selector_style = dict()
                        new_selector_style['selector'] = f"#{id}"
                        new_selector_style['style'] = style
                        stylesheet.append(new_selector_style)
                        element['classes'] += f' {id}'
                        element.pop('style', None)
                
        
        
        center_x = int(sum(dados["pos"][0] for dados in controller.classes.values()) / len(controller.classes))
        center_y = int(sum(dados["pos"][1] for dados in controller.classes.values()) / len(controller.classes))
        
        elements.append({
            'data': {'id': 'anchor'},
            'position': {'x': center_x, 'y': center_y},
            'classes': 'invisible'
        })

        print(f"window.center_x: {center_x}, window.center_y: {center_y}")
        
        dash_app.layout = html.Div([
            html.Button("Restaurar visualização", id="btn-reset-view", n_clicks=0),
            dcc.Store(id="camera-state", data={"pan": {'x': center_x, 'y': center_y}, "zoom": 1}),
            dcc.Store(id="dummy-store", data={"results": [], "currentIndex": 0}),
            dcc.Store(id="search-results-store", data={"results": [], "currentIndex": 0}),
            html.Div(id="debug-output", style={"position": "fixed", "top": "10px", "left": "200px", "background": "#eee", "padding": "5px", "zIndex": 9999}),
            html.Button(
                [
                    DashIconify(icon="mdi:magnify", width=20, height=20),
                ],
                id="btn-search",
                title="Pesquisar",
                n_clicks=0,
                style={
                    'padding': '8px',
                    'border': '1px solid #ccc',
                    'borderRadius': '4px',
                    'backgroundColor': '#f5f5f5',
                    'cursor': 'pointer',
                    'position': 'fixed',
                    'bottom': '15px',
                    'left': '357px',
                    'zIndex': 1001,
                    
                }
            ),
            html.Div([
            dcc.Input(
                id='search-input',
                placeholder='Search for a class...',
                type='text',
                style={'width': '300px', 'padding': '8px'},
                debounce=True,
                n_submit=0  # usado para capturar Enter
            ),
            dcc.RadioItems(
                id='radio-options',
                options=[
                    {'label': 'Palavra exata', 'value': 'exata'},
                    {'label': 'Palavra aproximada', 'value': 'aproximada'}
                ],
                value='exata',
                labelStyle={'display': 'inline-block', 'marginRight': '15px'}
            )
            ], style={
                'position': 'fixed',
                'bottom': '10px',
                'left': '10px',
                'zIndex': 1000,  # Garante que fique acima do Cytoscape
                'background': '#ffffff',
                'border': '1px solid #ccc',
                'color': 'black',
                'font-size': 10,
                'border-radius': '4px',
                'box-shadow': '0px 2px 4px rgba(0,0,0,0.2)',
                'padding': '10px',
                'display': 'flex',
                'flexDirection': 'column',
                'gap': '5px'
            }),
            cyto.Cytoscape(
                id='diagram',
                layout={'name': 'preset'},
                style={'width': '100%', 'height': '100vh'},
                elements=elements,
                stylesheet=stylesheet,
                zoom=1,
                pan={'x': center_x, 'y': center_y},
                wheelSensitivity=0.2
            )
        ])
        
        dash_app.clientside_callback(
            ClientsideFunction(namespace='clientside', function_name='restoreInitialView'),
            Output('camera-state', 'data'),
            Input('btn-reset-view', 'n_clicks'),
            prevent_initial_call=True
        )
               
        # # highlightSearchResults -> atualiza resultados
        # dash_app.clientside_callback(
        #     ClientsideFunction(namespace='clientside', function_name='highlight_and_focus_current_Result_with_button_search'),
        #     Output('search-results-store', 'data'),
        #     Input('btn-search', 'n_clicks'),
        #     Input('search-input', 'n_submit'),
        #     State('search-input', 'value'),
        #     State('radio-options', 'value'),
        #     prevent_initial_call=True
        # )
        
        #highlightSearchResults -> atualiza resultados
        # dash_app.clientside_callback(
        #     ClientsideFunction(namespace='clientside', function_name='highlightSearchResults'),
        #     Output('search-results-store', 'data'),
        #     Input('btn-search', 'n_clicks'),
        #     State('search-input', 'value'),
        #     State('radio-options', 'value'),
        #     State('dummy-store', 'data'),
        #     prevent_initial_call=True
        # )

        # # focusCurrentResult -> só lida com foco visual
        # dash_app.clientside_callback(
        #     ClientsideFunction(namespace='clientside', function_name='focusCurrentResult'),
        #     Output('dummy-store', 'data'),  # só pra forçar execução
        #     Input('search-input', 'n_submit'),
        #     Input('btn-search', 'n_clicks'),
        #     State('search-results-store', 'data'),
        #     prevent_initial_call=True
        # )

        # dash_app.clientside_callback(
        #     ClientsideFunction(namespace='clientside', function_name='highlightAndFocusResults'),
        #     Output('search-results-store', 'data'),
        #     Input('btn-search', 'n_clicks'),
        #     State('search-input', 'value'),
        #     State('radio-options', 'value'),
        #     prevent_initial_call=True
        # )
        
        # dash_app.clientside_callback(
        #     ClientsideFunction(namespace='clientside', function_name='focusCurrentResult'),
        #     Output('search-results-store', 'data'),
        #     Input('search-input', 'n_submit'),
        #     State('search-results-store', 'data'),
        #     prevent_initial_call=True
        # )
        
        dash_app.clientside_callback(
            ClientsideFunction(namespace='clientside', function_name='highlightAndNavigate'),
            Output('search-results-store', 'data'),
            Input('btn-search', 'n_clicks'),
            Input('search-input', 'n_submit'),
            State('search-input', 'value'),
            State('radio-options', 'value'),
            State('search-results-store', 'data'),
            prevent_initial_call=True
        )


        Thread(target=controller.run_server, daemon=True).start()
        qt_app = QApplication(sys.argv)
        window = MainWindow()
        window.center_x = center_x
        window.center_y = center_y
        window.show()
        sys.exit(qt_app.exec())