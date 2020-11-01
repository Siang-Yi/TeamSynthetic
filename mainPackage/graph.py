from math import inf

class Graph:
    def __init__(self, total_vertices, floor):
        self.vertices = [None] * total_vertices
        self.matrix = None
        for i in range(total_vertices):
            self.vertices[i] = Vertex(i)
            self.vertices[i].floor = floor
        self.locations = None
        self.floor = floor

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

    def shortest_link(self, current, vertices):
        link_map = {0: 15,
                    15: 0,
                    67: 75,
                    75: 67,
                    55: 56,
                    56: 55}
        shortest_dist = inf
        shortest_vertex = None
        for vertex in vertices:
            distance = self.matrix[current][vertex][0]
            if distance < shortest_dist:
                shortest_dist = distance
                shortest_vertex = vertex
        return shortest_vertex, link_map[shortest_vertex]

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
        for vertex_id in locations[self.floor].values():
            self.vertices[vertex_id].in_room = True

    def get_vertex(self, name, ground_floor):
        if ground_floor:
            if name in self.locations[0]:
                return self.locations[0][name], True, None
            else:
                return self.locations[1][name], False, [15, 75, 56]
        else:
            if name in self.locations[1]:
                return self.locations[1][name], True, None
            else:
                return self.locations[0][name], False, [0, 67, 55]

    def get_location_names(self):
        name_lst = []
        name_lst.append(list(self.locations[0].keys()))
        name_lst[0].sort()
        name_lst.append(list(self.locations[1].keys()))
        name_lst[1].sort()
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
        self.floor = None
        self.in_room = False

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
        [3, 4, 15],
        [3, 35, 10],
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

first_floor_edges = [[0, 1, 20],
                    [1, 2, 5],
                    [1, 3, 10],
                    [3, 4, 10],
                    [3, 35, 10],
                    [3, 5, 10],
                    [5, 6, 10],
                    [5, 8, 15],
                    [5, 7, 10],
                    [8, 9, 10],
                    [8, 10, 10],
                    [8, 11, 15],
                    [11, 12, 10],
                    [11, 13, 10],
                    [11, 14, 15],
                    [14, 15, 10],
                    [14, 16, 10],
                    [14, 17, 10],
                    [17, 18, 10],
                    [17, 19, 60],
                    [19, 20, 10],
                    [20, 21, 10],
                    [20, 22, 10],
                    [20, 23, 15],
                    [23, 24, 10],
                    [23, 25, 10],
                    [23, 26, 15],
                    [26, 27, 10],
                    [26, 28, 10],
                    [26, 29, 10],
                    [29, 30, 10],
                    [29, 31, 10],
                    [29, 32, 10],
                    [32, 33, 20],
                    [33, 34, 5],
                    [33, 35, 20],
                    [35, 36, 5],
                    [32, 37, 10],
                    [37, 38, 10],
                    [39, 40, 10],
                    [39, 41, 10],
                    [41, 42, 10],
                    [41, 43, 20],
                    [43, 45, 20],
                    [43, 67, 10],
                    [45, 44, 10],
                    [45, 46, 20],
                    [19, 46, 30],
                    [45, 47, 10],
                    [45, 48, 35],
                    [48, 49, 5],
                    [48, 51, 10],
                    [51, 52, 5],
                    [51, 54, 10],
                    [51, 53, 10],
                    [54, 55, 10],
                    [54, 56, 40],
                    [56, 57, 5],
                    [57, 59, 10],
                    [57, 58, 10],
                    [57, 60, 10],
                    [60, 61, 5],
                    [60, 62, 5],
                    [60, 63, 10],
                    [63, 64, 5],
                    [63, 65, 10],
                    [65, 66, 5],
                    [65, 41, 10]]

ground_vertices_coor = [[1.1691699196565253, 0.07675928484549388],  #0
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

first_vertices_coor = [[0.08554687500077307, 2.076364180353636],
[0.3246093750003354, 2.13843154489075],   
[0.34570312500136424, 2.0599686174595604],
[0.3117187500012335, 2.2707553764387143], 
[0.19921875000173372, 2.2812939310023523],
[0.3152343750013813, 2.3995545533360456], 
[0.20273437500046043, 2.4534124672454283],
[0.43007812500096065, 2.3468654104280375],
[0.30937500000106866, 2.5634631471168916],
[0.18632812500115392, 2.6255088526644244],
[0.4406250000014893, 2.510780466797641],
[0.3117187500012335, 2.7332034742523206],
[0.1945312500014893, 2.7858766957647276],
[0.42656250000078444, 2.6816985331211214],
[0.30937500000106866, 2.887704870267086],
[0.19335937500142109, 2.9532446338400007],
[0.43945312500139266, 2.8432293002009743],
[0.30820312500102887, 3.026972240807055],
[0.19570312500158593, 3.0562278441772577],
[0.9398437500016996, 3.029312718247553],
[0.9386718750015746, 2.8888752566065534],
[0.8097656250013756, 2.952074314578624],
[1.0675781250004377, 2.8420588671898486],
[0.9386718750015746, 2.72735075056643],
[0.8214843750004945, 2.784706205165321],
[1.0734375000006935, 2.675845560901351],
[0.9433593750004547, 2.5658045495701174],
[0.816796875001728, 2.6208262644830143],
[1.0687500000004775, 2.5096097162770548],
[0.9421875000003865, 2.401896246226272],
[0.8156250000016598, 2.456924865062831],
[1.07578125000083, 2.3445236243231022],
[0.9375000000015916, 2.2613877078454863],
[0.6644531250003922, 2.260216745013466],
[0.6691406250005798, 2.1442868281800287],
[0.42304687500066507, 2.2613877078454863],
[0.42304687500066507, 2.1419447175489097],
[1.0628906250016428, 2.2660715497172106],
[1.0664062500004263, 2.1536552348185865],
[1.2996093750011823, 2.2590457812369067],
[1.3031250000013301, 2.1489710386843512],
[1.4648437500016769, 2.271926330748002],
[1.4742187500006878, 2.1501420890663923],
[1.491796875001512, 2.562292444283642],
[1.3136718750004093, 2.7039395716321906],
[1.4378906250004206, 2.7905586465201964],
[1.3324218750012733, 3.024631758310832],
[1.4976562500017678, 2.9099420039426747],
[1.866796875001711, 2.809286262752096],
[1.852734375001063, 2.9029197984383046],
[1.878515625000773, 2.702769000793708],
[2.0332031250008242, 2.8057748575282204],
[2.044921875001336, 2.9029197984383046],
[2.046093750001404, 2.698086706154939],
[2.1855468750007674, 2.8069453271086786],
[2.17382812500162, 2.978991344717201],
[2.183203125000574, 2.315250968632114],
[2.091796875000682, 2.3187637193924644],
[2.078906250001495, 2.4171171519852663],
[2.1339843750011767, 2.1969833622670905],
[1.9523437500013756, 2.32578919473697],
[1.9500000000012676, 2.431167067373053],
[1.9699218750007788, 2.1969833622670905],
[1.8000000000014893, 2.323447373505388],
[1.8093750000004434, 2.1922993005386076],
[1.6300781250007503, 2.31759280344059],
[1.641796875001262, 2.198154375405039],
[1.695703125000989, 2.5681459477356157]]

all_floor_locations = [{"Main Lobby": 0,
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
                        "Elevator": 75},  # ground floor
                        {"Janitor": 2,
                        "Patient RM.A5": 4,
                        "Patient RM.A6": 6,
                        "Patient RM.A7": 9,
                        "Patient RM.A8": 12,
                        "Patient RM.A9": 15,
                        "Patient RM.A1": 7,
                        "Patient RM.A2": 10,
                        "Patient RM.A3": 13,
                        "Patient RM.A4": 16,
                        "Electrical": 18,
                        "Patient RM.B1": 30,
                        "Patient RM.B2": 27,
                        "Patient RM.B3": 24,
                        "Patient RM.B4": 21,
                        "Med Storage Records": 22,
                        "Nurse Office 1-2": 25,
                        "Nurse Office 1-1": 28,
                        "Staff Break Room": 31,
                        "M.Restroom": 36,
                        "W.Restroom": 34,
                        "Conference Room": 38,
                        "Doctor's Office 1-1": 40,
                        "Doctor's Office 1-2": 42,
                        "Patient RM.D1": 66,
                        "Patient RM.D2": 64,
                        "Patient RM.D3": 62,
                        "Patient RM.D4": 59,
                        "Office 1-3": 61,
                        "Office 1-4": 50,
                        "Office 1-5": 58,
                        "Office 1-6": 53,
                        "Patient RM.D6": 52,
                        "Patient RM.D5": 49,
                        "Storage": 47,
                        "Elevator": 67}]

all_floor_locations_area = [{"Main Lobby": [[0.22598442355946702, 1.0628906250011028], [0.053719376611439884, 1.3218750000001478]],
                        "Waiting Room": [[0.20371895524260708, 0.6585937500009607], [0.024422508742389937, 0.9890625000004718]],
                        "Reception": [[0.33848304060771284, 1.0464843750003183], [0.24824985774786512, 1.3218750000001478]],
                        "Dialysis G-1": [[0.4205124842290502, 0.6996093749999659], [0.311530349484471, 0.9164062499999943]],
                        "Dialysis G-2": [[0.5306649224150419, 0.6972656249998863], [0.4216843275792712, 0.9187500000000739]],
                        "Pharmacy Pick Up": [[0.25528103986268036, 0.4101562500009095], [0.09121934594632819, 0.5472656250000512]],
                        "Pharmacy": [[0.4228561707530787, 0.4113281250009493], [0.2658278057920427, 0.5472656250000512]],
                        "Nurse Office G-1": [[0.25645290317756064, 0.2753906250003979], [0.08887559884091445, 0.4078125000008015]],
                        "Nurse Office G-2": [[0.41934064070298405, 0.27187500000019327], [0.25879662948503324, 0.4101562500009095]],
                        "Emergency Ward 1": [[0.3502015789538575, 4.831690603168681e-13], [0.1486410927492301, 0.16523437500100613]],
                        "Doctor's Office G-1": [[0.645502603867115, 0.2753906250003979], [0.5341803956267341, 0.5472656250000512]],
                        "Doctor's Office G-2": [[0.7603376921552467, 0.2753906250003979], [0.6466744043622015, 0.5460937500000114]],
                        "Emergency Ward 2": [[0.7767424661874429, 0.003515625000630962], [0.6056612295896997, 0.16523437500100613]],
                        "Emergency Ward 3": [[0.9407864823073879, 0.005859375000767386], [0.7802577666696919, 0.16406250000096634]],
                        "Emergency Ward 4": [[1.0743595457294788, 0.007031250000835598], [0.9443016316190409, 0.16289062500089813]],
                        "Surgery G-1": [[1.0708445367456392, 0.2765625000004377], [0.877513201915022, 0.4945312500005059]],
                        "Surgery G-2": [[1.0743595457294788, 0.4910156250003581], [0.8739979875775248, 0.7101562500004661]],
                        "Consult RM. 1": [[0.25293731291303345, 1.3699218750009834], [0.09004747241246491, 1.5375000000001648]],
                        "Consult RM. 2": [[0.25293731291303345, 1.533984375000017], [0.08653185158678411, 1.7027343750006878]],
                        "Consult RM. 3": [[0.2541091764410197, 1.7015625000006196], [0.08653185158678411, 1.8667968750011426]],
                        "Consult RM. 4": [[0.25645290317756064, 1.8632812500009948], [0.09239121944202111, 2.034375000000267]],
                        "X-Ray RM. G-1": [[0.25645290317756064, 2.0320312500001876], [0.09004747241246491, 2.1421875000010004]],
                        "ATM Machines": [[0.4744170883267742, 1.8328125000009834], [0.3783260102795083, 1.9933593749997556]],
                        "Retail 2": [[0.5142593545588454, 2.0859374999997726], [0.3689512096311063, 2.244140624999943]],
                        "Retail 1": [[0.6724539459471259, 2.0882812499999375], [0.516603009722516, 2.248828125000159]], 
                        "Convenience Store": [[0.6466744043622015, 1.8316406250009436], [0.48027625997441703, 1.9921875000011937]],
                        "Florist": [[0.7603376921552467, 1.8292968750007788], [0.6490180045402667, 1.9933593749997556]],
                        "Surgery G-4": [[1.075531214492699, 1.839843749999858], [0.8763414641688598, 2.0882812499999375]],
                        "Surgery G-3": [[1.0743595457294788, 1.5890625000011198], [0.877513201915022, 1.8410156249998977]],
                        "Pre-Op RM. G-2": [[1.0720162068554089, 1.4261718750007049], [0.8786849392940752, 1.592578124999818]],
                        "Pre-Op RM. G-1": [[1.075531214492699, 1.2621093750002785], [0.8739979875775248, 1.425000000000665]],
                        "W.Restroom": [[1.0743595457294788, 0.9585937500005173], [0.9349278922556294, 1.2058593750005286]],
                        "M.Restroom": [[1.075531214492699, 0.7125000000006025], [0.9314127335282052, 0.9609375000006537]],
                        "Cafeteria": [[0.851734887584044, 0.7441406250005969], [0.604489419935959, 1.1390625000003354]],
                        "Admin Office": [[0.7673683173087937, 1.2597656250001705], [0.5330085714456487, 1.425000000000665]],
                        "Elevator": [[0.7591659201802656, 1.533984375000017], [0.3701230602575407, 1.8246093750005343]]},  # ground floor
                        {"Janitor": 2,
                        "Patient RM.A5": 4,
                        "Patient RM.A6": 6,
                        "Patient RM.A7": 9,
                        "Patient RM.A8": 12,
                        "Patient RM.A9": 15,
                        "Patient RM.A1": 7,
                        "Patient RM.A2": 10,
                        "Patient RM.A3": 13,
                        "Patient RM.A4": 16,
                        "Electrical": 18,
                        "Patient RM.B1": 30,
                        "Patient RM.B2": 27,
                        "Patient RM.B3": 24,
                        "Patient RM.B4": 21,
                        "Med Storage Records": 22,
                        "Nurse Office 1-2": 25,
                        "Nurse Office 1-1": 28,
                        "Staff Break Room": 31,
                        "M.Restroom": 36,
                        "W.Restroom": 34,
                        "Conference Room": 38,
                        "Doctor's Office 1-1": 40,
                        "Doctor's Office 1-2": 42,
                        "Patient RM.D1": 66,
                        "Patient RM.D2": 64,
                        "Patient RM.D3": 62,
                        "Patient RM.D4": 59,
                        "Office 1-3": 61,
                        "Office 1-4": 50,
                        "Office 1-5": 58,
                        "Office 1-6": 53,
                        "Patient RM.D6": 52,
                        "Patient RM.D5": 49,
                        "Storage": 47,
                        "Elevator": 67}]


# for key, item in all_floor_locations_area[0].items():
#     print(item)

ground_floor_graph = Graph(77, 0)
for i in range(len(ground_vertices_coor)):
    ground_floor_graph.vertices[i].coor = ground_vertices_coor[i]

ground_floor_graph.add_edges(groud_floor_edges)
ground_floor_graph.floyd_warshall()
ground_floor_graph.add_locations(all_floor_locations)

first_floor_graph = Graph(68, 1)
for i in range(len(first_vertices_coor)):
    first_floor_graph.vertices[i].coor = first_vertices_coor[i]

first_floor_graph.add_edges(first_floor_edges)
first_floor_graph.floyd_warshall()
first_floor_graph.add_locations(all_floor_locations)