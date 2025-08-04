class Ship:
    def __init__(self, name, size, symbol, start_position=None, orientation='horizontal'):
        self.name = name
        self.size = size
        self.symbol = symbol
        self.start_position = start_position
        self.orientation = orientation
        self.positions = []  #liste des vases occupées par le bateau
        self.hits = []    # Liste des cases où le bateau a été touché
        
    def place(self, start_position, orientation):
        self.start_position = start_position
        self.orientation = orientation
        self.positions = self._calculate_positions()   #calcule les positions
        return self.positions
    
    def _calculate_positions(self):
        if not self.start_position:
            return []
            
        positions = []
        row = self.start_position[0]  #représente la lettre
        col = int(self.start_position[1:])  #représente le numéro
        
        for i in range(self.size):
            if self.orientation == 'horizontal':
                new_col = col + i   #si placement est horizontal alors on augmente le numéro de colonne --> le bateau sera postitionné horizontalement
                if new_col <= 10:
                    positions.append(f"{row}{new_col}")
            else:
                row_index = ord(row) - ord('A') + i    #idem mais avec la lettre de la ligne
                if row_index < 10:  
                    new_row = chr(ord('A') + row_index)
                    positions.append(f"{new_row}{col}")
                    
        return positions if len(positions) == self.size else []  #retourne les positions si le bateau rentre entièrement dans les cases demandées
    
    def is_valid_placement(self, grille, other_ships=[]):
        positions = self._calculate_positions()
        
        if len(positions) != self.size:     #vérifie que le bateau rentre entièrement
            return False
            
        for pos in positions:             #vérifie que la position demandée du bateau existe dans le grille
            if pos not in grille:
                return False
                
            for ship in other_ships:       #vérifie que la poisition demandée n'est pas déjà occupée par un autre bateau
                if pos in ship.positions:
                    return False
                    
        return True
    
    def hit(self, position):    #vérifie si le bateau à été touché et ajoute les cases touchées dans la liste self.hits
        if position in self.positions and position not in self.hits:
            self.hits.append(position)
            return True
        return False
    
    def is_sunk(self):
        return len(self.hits) == self.size
    
    def get_unhit_positions(self):
        return [pos for pos in self.positions if pos not in self.hits]


def create_fleet():
    return [
        Ship("Porte-avions", 5, "P"),
        Ship("Croiseur", 4, "C"),
        Ship("Contre-torpilleur", 3, "D"),
        Ship("Sous-marin", 3, "S"),
        Ship("Torpilleur", 2, "T")
    ]