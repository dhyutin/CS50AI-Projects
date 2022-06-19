import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if(len(self.cells) == self.count):
            return self.cells
        else:
            return set()        
        # raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if(self.count == 0):
            return self.cells
        else:
            return set()
        # raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1
            return
        else:
            return

        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            return
        else:
            return
        # raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def inference(self):
        for i in self.knowledge:
            for j in self.knowledge:
                if i.cells.issubset(j.cells):
                    # New Sentence
                    new_count = i.count - j.count
                    new_cells = i.cells - j.cells
                    new_sentence = Sentence(new_cells, new_count)

                    mines = new_sentence.known_mines()
                    safes = new_sentence.known_safes()

                    if mines:
                        for mine in mines:
                            self.mark_mine(mine)
                    if safes:
                        for safe in safes:
                            self.mark_safe(safe)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1 : Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2 : Mark the cell as safe 
        self.mark_safe(cell)

        # 3 : Add a new sentence to AI's knowledge base based on the value of 'cell' and 'count'
        # Firstly, necessary updations about marking the cell as safe have to be made
        
        # Find Neighbours
        cell_neighbours = set()
        i = cell[0]
        j = cell[1]
        
        neighbours = [(i+1,j-1), (i+1, j), (i+1, j+1), (i, j-1), (i, j+1), (i-1, j-1), (i-1, j), (i-1, j+1)]

        for a, b in neighbours:
            if((a in range(self.height)) and (b in range(self.width))) :
                cell_neighbours.add((a, b))

        # Find new_ count and new cells for sentence
        cells_new = set()
        count_new = count

        for i in cell_neighbours:
            if i in self.mines:
                count_new = count_new - 1
            elif ((i not in self.mines) and (i not in self.safes)):
                cells_new.add(i)

        # Add new sentence
        sentence_new = Sentence(cells_new, count_new)

        if (len(sentence_new.cells) > 0):
            self.knowledge.append(sentence_new)

        # 4 : Mark additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        for sentence in self.knowledge:
            if(len(sentence.cells) == 0):
                self.knowledge.remove(sentence)
        safes = list(sentence.known_safes())
        for safe in safes:
            self.mark_safe(safe)

        mines = list(sentence.known_mines())
        for mine in mines:
            self.mark_mine(mine)
        
        
        # 5 : Add Inferences if any
        self.inference()               

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for i in self.safes - self.moves_made:
            return i      

        return None  
        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        num_moves_possible = self.width * self.height

        while num_moves_possible > 0:

            row = random.randrange(self.height)
            column = random.randrange(self.width)

            if (((row, column) not in self.moves_made) and ((row, column) not in self.mines)):
                return (row, column)
            num_moves_possible = num_moves_possible - 1
        return None
        # raise NotImplementedError
