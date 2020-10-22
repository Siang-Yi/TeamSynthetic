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
        return list(self.locations.keys())

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


ground_floor_graph = Graph(35)

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
        [17, 33, 10]]

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
[0.31732146914242776, 0.1998036790296993]]

first_floor_locations = {"Waiting Room": 2,
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
                        "Surgery G-2": 30}

for i in range(len(vertices_coor)):
    ground_floor_graph.vertices[i].coor = vertices_coor[i]

ground_floor_graph.add_edges(groud_floor_edges)
ground_floor_graph.floyd_warshall()
ground_floor_graph.add_locations(first_floor_locations)