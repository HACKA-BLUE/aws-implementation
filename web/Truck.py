import math

class Truck:
    def __init__(self, id, dumpster, truck_type):
        self.id = id
        self.current_position = dumpster
        self.dir = (0,0)
        self.truck_type = truck_type
        self.containers = []
        self.serving = False
        self.returning = False
        self.path = []
    
    def get_next_node(self):
        if (len(self.containers) == 0):
            return ""
        elem = self.containers[0]
        self.containers = self.containers[1:]
        return elem
    
    def set_pathing(self, path):
        self.serving = True
        self.destination = [path[0]["lat"], path[0]["lon"]]
        self.dir = (self.current_position[1] - self.destination[1], self.current_position[0] - self.destination[0])
        self.path = path[1:]
    
    def get_path(self):
        return self.path

    def add_cont(self, container):
        self.containers.append(container)
    
    def is_serving(self):
        return self.serving

    def move(self, speed):        
        dx, dy = self.dir
        distance = math.sqrt(dx**2 + dy**2)
        
        # If the distance is smaller than or equal to speed, snap to destination
        if distance <= speed:
            self.current_position = self.destination
            if (len(self.path) == 0):
                if (self.returning):
                    self.serving = False
                #TODO : else containers have containers to serve 
            else:
                self.destination = self.path[0]
                self.path = self.path[1:]
            return True
        
        # Calculate the normalized direction vector
        new_x = (dx / distance) * speed
        new_y = (dy / distance) * speed
        
        # Update the current position by moving along the direction vector
        self.current_position = (self.current_position[0] + new_x, self.current_position[1] + new_y)
        
        return False
    
    def return_to_base(self, dumpster):
        self.returning = True
        x0, y0 = self.current_position
        x1, y1 = dumpster
        self.dir = (x1 - x0, y1 - y0)

    def set_destination(self, next_container):
        x0, y0 = self.current_position
        x1, y1 = next_container.get_coord()
        self.dir = (x1 - x0, y1 - y0)

    def get_type(self):
        return self.truck_type
    
    def get_id(self):
        return self.id

    def get_coord(self):
        return self.current_position
    
    def set_coord(self, new_pos):
        self.current_position = new_pos

    def get_containers(self):
        return self.containers
    
    def set_containers(self, containers):
        self.containers = containers

    def add_to_container(self, container):
        self.containers.append(container)