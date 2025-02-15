class Container:
    def __init__(self, id, limit, longitude, latitude, container_type):
        self.id = id
        self.limit = limit
        self.cards_passed = 0
        self.longitude = longitude
        self.latitude = latitude
        self.container_type = container_type

    def card_passed(self):
        if (self.cards_passed > self.limit):
            return False
        self.cards_passed += 1
        return self.cards_passed > self.limit / 2
    
    def get_cards(self):
        return self.cards_passed

    def get_id(self):
        return self.id
    
    def get_coord(self):
        return (self.latitude, self.longitude)
    
    def get_type(self):
        return self.container_type
    
    def toString(self):
        return(f"{self.id}, {self.limit}, {self.longitude}, {self.latitude}, {self.container_type}")

    def get_cards_passed(self):
        if (self.cards_passed < self.limit / 3):
            return "low"
        elif (self.cards_passed < self.limit / 2):
            return "medium"
        return "high"
