from math import inf

class Graph:
    def __init__(self, total_vertices):
        self.vertices = [None] * total_vertices
        self.matrix = None
        for i in range(total_vertices):
            self.vertices[i] = Vertex(i)
        self.locations = None

    def add_edges(self, argv_edges):
        for edge in argv_edges:
            u, v, w = edge
            current_edge = Edge(u, v, w)
            current_vertex = self.vertices[u]
            current_vertex.add_edge(current_edge)
            current_edge = Edge(v, u, w)
            current_vertex = self.vertices[v]
            current_vertex.add_edge(current_edge)

    def generate_matrix(self):
        self.matrix = [[[inf, None] for i in range(len(self.vertices))] for j in range(len(self.vertices))]
        for vertex in self.vertices:
            for edge in vertex.edges:
                self.matrix[edge.u][edge.v][0] = edge.w
                self.matrix[edge.v][edge.u][0] = edge.w
        

    def floyd_warshall(self):
        self.generate_matrix()
        for k in range(len(self.matrix)):
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix)):
                    if (self.matrix[i][k][0] + self.matrix[k][j][0]) < self.matrix[i][j][0]:
                        self.matrix[i][j][0] = self.matrix[i][k][0] + self.matrix[k][j][0]
                        self.matrix[i][j][1] = k
    
    def path(self, start_vertex, end_vertex):
        last = self.matrix[start_vertex][end_vertex]
        between = []
        all_path = [start_vertex] + self.recursive_find(start_vertex, end_vertex, between) + [end_vertex]
        return all_path

    def recursive_find(self, start, end, between):
        if self.matrix[start][end][1] == None:
            return []
        else:
            mid = self.matrix[start][end][1]
            left = self.recursive_find(start, mid, between)
            between.append(mid)
            right = self.recursive_find(mid, end, between)
            return between
    
    def add_locations(self, locations):
        self.locations = locations

    def get_vertex(self, name):
        return self.locations[name]

    def get_location_names(self):
        name_lst = list(self.locations.keys())
        name_lst.sort()
        return name_lst

    def __str__(self):
        return_string = ""
        for vertex in self.vertices:
            return_string += str(vertex) + "\n"
        return return_string


class Vertex:
    def __init__(self, id):
        self.ppl_count = 0
        self.coor = None
        self.id = id
        self.discovered = False
        self.visited = False
        self.distance = 0
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)
 
    def set_room_name(self, name):
        self.room_name = name

    def __str__(self):
        return_string = "Vertex: " + str(self.id) + " Coor: " + str(self.coor) + "\n"
        for edge in self.edges:
            return_string += str(edge) + "\n"
        return return_string


class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def __str__(self):
        return str(self.u) + ", " + str(self.v) + ", " + str(self.w)


ground_floor_graph = Graph(77)

groud_floor_edges = [[0, 1, 15],
        [1, 2, 10],
        [0, 3, 20],
        [0, 4, 25],
        [4, 5, 5],
        [4, 9, 30],
        [5, 8, 10],
        [5, 6, 5],
        [6, 7, 10],
        [9, 10, 20],
        [9, 11, 20],
        [9, 12, 15],
        [9, 13, 15],
        [10, 19, 35],
        [10, 29, 30],
        [11, 14, 35],
        [14, 15, 10],
        [14, 16, 10],
        [16, 17, 10],
        [17, 18, 10],
        [17, 19, 15],
        [19, 20, 10],
        [20, 21, 10],
        [20, 32, 10],
        [20, 22, 10],
        [22, 31, 10],
        [22, 23, 10],
        [23, 24, 10],
        [23, 27, 15],
        [23, 25, 15],
        [25, 26, 10],
        [27, 28, 10],
        [27, 29, 15],
        [29, 30, 10],
        [16, 34, 10],
        [17, 33, 10],  # first half
        [0, 35, 20],
        [35, 36, 10],
        [36, 37, 5],
        [36, 38, 15],
        [38, 39, 5],
        [38, 40, 15],
        [40, 41, 5],
        [40, 42, 15],
        [42, 43, 5],
        [42, 44, 10],
        [44, 45, 5],
        [42, 47, 10],
        [44, 45, 5],
        [44, 46, 10],
        [42, 47, 10],
        [46, 47, 10],
        [46, 48, 10],
        [46, 49, 15],
        [49, 50, 10],
        [49, 51, 10],
        [49, 52, 10],
        [52, 53, 5],
        [52, 54, 10],
        [54, 55, 10],
        [55, 56, 10],
        [55, 57, 15],
        [57, 58, 5],
        [57, 59, 20],
        [59, 60, 10],
        [59, 61, 15],
        [61, 62, 5],
        [61, 63, 10],
        [63, 64, 5],
        [65, 66, 10],
        [66, 67, 5],
        [68, 69, 5],
        [68, 70, 15],
        [70, 71, 25],
        [71, 6, 15],
        [6, 72, 20],
        [72, 65, 20],
        [72, 73, 10],
        [36, 74, 20],
        [74, 75, 15],
        [63, 76, 10]]

vertices_coor = [[1.1691699196565253, 0.07675928484549388],  #0
[1.02404018364237, 0.1019992080205867],
[0.9104603902406438, 0.10830918591202021],
[1.1817898967007068, 0.30707241883195024],
[0.9893352467698264, 0.2723679261727341],
[0.9704052812028863, 0.3607064086110654],
[0.9830252582483752, 0.47428316814645655],
[0.8631354763239472, 0.47743805359456815],
[0.8662904705853123, 0.3607064086110654],
[0.6138909296921895, 0.25659312298300563],
[0.6233559124750627, 0.47428316814645655],  # 10
[0.5918059698638842, 0.04520936050435864],
[0.48769115924503126, 0.3323119798228191],
[0.48769115924503126, 0.1871837739739135],
[0.2163616527862473, 0.06729430955094529],
[0.09647187086176245, 0.06729430955094529],
[0.23213662409179392, 0.2029586538016872],
[0.21320665852485376, 0.30076251908184304],
[0.09331687660039734, 0.30076251908184304],
[0.2289816298304288, 0.47428316814645655],
[0.21951664704633345, 0.6004773624358251],  # 20
[0.09962686512318442, 0.654109048449186],
[0.22267164130769856, 0.7140496641511191],
[0.21951664704633345, 0.8213098249227215],
[0.10278185938454953, 0.8244644937995105],
[0.2163616527862473, 0.9916581302353649],
[0.09962686512318442, 0.9853490807894474],
[0.342561423232155, 0.8150004797099655],
[0.35833639453773003, 0.9317216857860586],
[0.5854959813411256, 0.8150004797099655],
[0.5791859928197027, 0.9380308343585],  # 30
[0.3394064289707899, 0.7077401613208423],
[0.33309644044805964, 0.5910128912991297],
[0.3204764634038213, 0.3102273673151785],
[0.31732146914242776, 0.1998036790296993],
[1.3031249999990564, 0.2859363130998531],
[1.4964843749993975, 0.31288906982958054],
[1.5011718749981924, 0.2203119571003498], 
[1.6628906249985391, 0.2964830518597381], 
[1.6605468749984595, 0.2167963576775378], 
[1.8222656249987779, 0.3011704881051429],  # 40
[1.8246093749988574, 0.20859328920755615],
[1.994531249998147, 0.3070297805721083],  
[1.994531249998147, 0.20976515639777915], 
[2.101171874998812, 0.3070297805721083],
[2.109374999999204, 0.2144526242746423],
[2.026171874998198, 0.4148401254722245],
[1.9253906249992383, 0.4148401254722245],
[2.1386718749991473, 0.39843428871432707],
[2.0390624999988347, 0.5648346009095633],
[1.9546874999991815, 0.6105353205794586],  # 50
[2.131640624998795, 0.5437418380957553],
[2.042578124998954, 0.7113098525533417],
[1.931249999998073, 0.7159969889428481],
[2.178515624998113, 0.719512338092045],
[2.1667968749990223, 0.820284476704046],
[2.178515624998113, 0.9866699801484771],
[1.8996093749994714, 0.8167692104493369],
[1.8972656249993918, 0.9280844123026242],
[1.664062499998579, 0.8191127216282581],
[1.6664062499987153, 0.9292561333739684],  # 60
[1.5222656249991644, 0.8226279858258181],
[1.5410156249986073, 0.9269126908430962],
[1.3804687499983572, 0.820284476704046],
[1.3804687499983572, 0.9210540777415304],
[1.2339843749987267, 0.8659826521967773],
[1.1484374999990337, 0.9058216387537925],
[1.1589843749981128, 0.9655792913755334],
[0.9128906249981696, 0.9034781808918524],
[0.918749999998397, 0.9772963570316051],
[0.7453124999989598, 0.896447798252467],  # 70
[0.9398437499994259, 0.7124816370982217],
[1.2046874999987836, 0.5753809537889651],
[1.3207031249984311, 0.5706936882281468],
[1.4742187499983856, 0.5695218712398713],
[1.7027343749989257, 0.562490964324823],
[1.380468750000034, 0.7216690519966704]]

first_floor_locations = {"Main Lobby": 0,
                        "Waiting Room": 2,
                        "Reception": 3,
                        "Dialysis G-1": 8,
                        "Dialysis G-2": 7,
                        "Pharmacy Pick Up": 13,
                        "Pharmacy": 12,
                        "Nurse Office G-1": 34,
                        "Nurse Office G-2": 33,
                        "Emergency Ward 1": 18,
                        "Doctor's Office G-1": 32,
                        "Doctor's Office G-2": 31,
                        "Emergency Ward 2": 21,
                        "Emergency Ward 3": 24,
                        "Emergency Ward 4": 26,
                        "Surgery G-1": 28,
                        "Surgery G-2": 30,
                        "Consult RM. 1": 37,
                        "Consult RM. 2": 39,
                        "Consult RM. 3": 41,
                        "Consult RM. 4": 43,
                        "X-Ray RM. G-1": 45,
                        "ATM Machines": 47,
                        "Retail 2": 48,
                        "Retail 1": 51,
                        "Convenience Store": 50,
                        "Florist": 53,
                        "Surgery G-4": 58,
                        "Surgery G-3": 60,
                        "Pre-Op RM. G-2": 62,
                        "Pre-Op RM. G-1": 64,
                        "W.Restroom": 67,
                        "M.Restroom": 69,
                        "Cafeteria": 71,
                        "Admin Office": 73,
                        "Elevator": 75}

for i in range(len(vertices_coor)):
    ground_floor_graph.vertices[i].coor = vertices_coor[i]

ground_floor_graph.add_edges(groud_floor_edges)
ground_floor_graph.floyd_warshall()
ground_floor_graph.add_locations(first_floor_locations)