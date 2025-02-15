from flask import Flask, jsonify, request
from flask_cors import CORS
import queue, random
import mysql.connector
from mysql.connector import Error
from Container import Container
from Truck import Truck
import osmnx as ox
import networkx as nx

app = Flask(__name__)
CORS(app)

# Definir los tipos de basura (0-4)
tipos_basura = ["waste", "cardboard", "glass", "organic", "plastic"]



# Conectar a MySQL
try:
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    if connection.is_connected():
        print("✅ Conectado a MySQL:", connection.get_server_info())
except Error as e:
    print("❌ Error al conectar con MySQL:", e)

# Definir los tipos de basura (0-4)
tipos_basura = ["waste", "cardboard", "glass", "organic", "plastic"]

camiones = {}   # Declarar diccionario de camiones
contenedores = {
    "waste": [],
    "cardboard": [],
    "glass": [],
    "organic": [],
    "plastic": []
} # Declarar diccionario de contenedores


cursor = connection.cursor()

cursor.execute("SELECT * FROM dumpster")
for row in cursor.fetchall():
    dump = [float(row[1]), float(row[2])]

cursor.execute("SELECT * FROM truck;")
for row in cursor.fetchall():
    camiones[row[0]] = Truck(row[0], dump, row[0])

cursor.execute("SELECT * FROM containers;")
for row in cursor.fetchall():
    id_, address, container_type, priority, lat, lon, count = row  # Extraer valores de la fila

    # 📌 Convertir coordenadas a float para evitar errores
    lat = float(lat)
    lon = float(lon)

    # 📌 Asignar al tipo correcto en el diccionario
    if container_type == "waste":
        contenedores["waste"].append(Container(id_, 60, lon, lat, "waste"))
    elif container_type == "cardboard":
        contenedores["cardboard"].append(Container(id_, 60, lon, lat, "cardboard"))
    elif container_type == "glass":
        contenedores["glass"].append(Container(id_, 60, lon, lat, "glass"))
    elif container_type == "organic":
        contenedores["organic"].append(Container(id_, 60, lon, lat, "organic"))
    elif container_type == "plastic":
        contenedores["plastic"].append(Container(id_, 60, lon, lat, "plastic"))


# Capacidad de llenado aleatoria para cada contenedor
capacidad_opciones = ["low", "medium", "high"]


@app.route('/camiones', methods=['GET'])
def obtener_camiones():
    """ Devuelve la posición de los camiones según los tipos seleccionados """
    tipos = request.args.get("tipos")
    if not tipos:
        return jsonify({"error": "Debe proporcionar al menos un tipo de camión"}), 400

    tipos_seleccionados = list(map(int, tipos.split(",")))  # Convertir a enteros
    resultado = {}

    for tipo_id in tipos_seleccionados:
        camion = camiones[tipo_id]
        if (camion.is_serving()):
            if (camion.move(0.0001)):
                # If here we have arrived at destination. get next node
                origen = camion.get_coord()
                node = camion.get_next_node()
                if (node == ""):
                    # no more nodes, go to dumptser
                    print(origen)
                    print(dump)
                    camion.set_pathing(ruta_mas_corta(origen[0], origen[1], dump[0], dump[1]))
                    camion.return_to_base()
                else:
                    # pathfind next node
                    dest = node.get_coord()
                    origen = camion.get_coord()
                    camion.set_pathing(ruta_mas_corta(origen[0], origen[1], dest[0], dest[1]))

        x, y = camion.get_coord()
        resultado[tipo_id] = {
            "lat": x,
            "lon": y
        }

    return jsonify(resultado)

@app.route('/contenedores', methods=['GET'])
def obtener_contenedores():
    """ Devuelve la posición, capacidad y tipo de los contenedores seleccionados """
    tipos = request.args.get("tipos")
    if not tipos:
        return jsonify({"error": "Debe proporcionar al menos un tipo de contenedor"}), 400
    
    tipos_seleccionados = tipos.split(",")
    resultado = []

    for tipo in tipos_seleccionados:
        for contenedor in contenedores[tipo]:
            resultado.append({
                "lat": contenedor.get_coord()[0],
                "lon": contenedor.get_coord()[1],
                "tipo": contenedor.get_type(),
                "capacidad": contenedor.get_cards_passed()
            })

    return jsonify(resultado)

@app.route('/update-container', methods=['GET'])
def update_container():
    values = request.args.get("id")
    for value in contenedores.values():
        for container in value:
            if (container.get_id() == int(values)):
                if (container.card_passed()):
                    search_truck(container)
                print("cards " + str(container.get_cards()))
                return ""
    return ""

G = ox.graph_from_place("Tarragona, Spain", network_type="drive")

def search_truck(container):
    print("i get here")
    for i in range(len(tipos_basura) - 1):
        if (tipos_basura[i] == container.get_type()):
            index = i
    camion = camiones[index]
    if (len(camion.get_path()) == 0):
        # no route TODO :
        path = ruta_mas_corta(camion.get_coord()[0], camion.get_coord()[1], container.get_coord()[0], container.get_coord()[1])
        camion.set_pathing(path)
    else:
        camion.add_cont(container)


def ruta_mas_corta(lat_origen, lon_origen, lat_destino, lon_destino):

        nodo_inicio = ox.distance.nearest_nodes(G, X=lon_origen, Y=lat_origen)
        nodo_destino = ox.distance.nearest_nodes(G, X=lon_destino, Y=lat_destino)

        print(f"🚛 Nodo inicial: {nodo_inicio}, Nodo destino: {nodo_destino}")

        try:
            ruta = nx.shortest_path(G, nodo_inicio, nodo_destino, weight="length")
        except nx.NetworkXNoPath:
            print("No se encontró una ruta entre los puntos dados.")
            return []
        
        fig, ax = ox.plot.plot_graph_route(G, ruta, node_size=0)
        fig.savefig("ruta_tarragona.png", dpi=300, bbox_inches='tight')

        ruta_coords = [{"lat": G.nodes[n]["y"], "lon": G.nodes[n]["x"]} for n in ruta]

        return ruta_coords

@app.route('/test', methods=['GET'])
def test():
    # start point
    start_point = dump

    # end point
    end_point = contenedores["waste"][0].get_coord()
    print(end_point)

    G = ox.graph_from_place("Tarragona, Spain", network_type="drive")

    def ruta_mas_corta(lat_origen, lon_origen, lat_destino, lon_destino):

        nodo_inicio = ox.distance.nearest_nodes(G, X=lon_origen, Y=lat_origen)
        nodo_destino = ox.distance.nearest_nodes(G, X=lon_destino, Y=lat_destino)

        print(f"🚛 Nodo inicial: {nodo_inicio}, Nodo destino: {nodo_destino}")

        try:
            ruta = nx.shortest_path(G, nodo_inicio, nodo_destino, weight="length")
        except nx.NetworkXNoPath:
            print("No se encontró una ruta entre los puntos dados.")
            return []

        ruta_coords = [{"lat": G.nodes[n]["y"], "lon": G.nodes[n]["x"]} for n in ruta]

        return ruta_coords
    
    route = ruta_mas_corta(start_point[0], start_point[1], end_point[0], end_point[1])
    #print(route)

#test()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)


