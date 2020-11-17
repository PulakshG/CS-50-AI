import itertools
import random
import copy


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
        if ( self.count == len(self.cells) ):
            return self.cells
        #raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if ( self.count == 0 ):
            return self.cells
        #raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count-=1

        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.cells.discard(cell)

        #raise NotImplementedError


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
        self.moves_made.add(cell) #1
        self.safes.add(cell) #2
        new_sentence = Sentence(self.nearby_mines(cell),count) #3

        length=len(new_sentence.cells)
        self.knowledge_append(new_sentence) #4

        self.inferred(new_sentence)      #5

        #raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        move_space=set()
        move_space=move_space.union(self.safes)
        move_space=move_space.difference(self.moves_made)
        if len(move_space)!=0:
            return move_space.pop()
        else:
            return None
        #raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        move_space=set()
        for i in range(self.height):
            for j in range(self.width):
                move_space.add(tuple((i,j)))
        move_space=move_space.difference(self.moves_made)
        move_space=move_space.difference(self.mines)
        if len(move_space)!=0:
            return move_space.pop()
        else:
            return None
        #raise NotImplementedError

    def nearby_mines(self, cell):
        """
        Returns a set of neighbors on the board.
        """

        # Keep count of nearby mines
        neighbors = set()
        x, y = cell
        # Loop over all cells within one row and column
        for i in self.permitted_values(x,0):
            for j in self.permitted_values(y,1):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                if tuple((i, j)) in self.moves_made:
                    continue
                neighbors.add(tuple((i,j)))

        return neighbors

    def permitted_values(self,x,variable):
        if variable == 0:
            limit = self.width-1
        elif variable == 1:
            limit = self.height-1
        if x in range(1,limit):
            return [x-1,x,x+1]
        elif x==0:
            return [x,x+1]
        elif x==7:
            return [x-1,x]

    def all_mine(self,sentence):
        if len(sentence.cells)==sentence.count:
            for i in sentence.cells:
                self.mark_mine(i)
            return True
        return False

    def no_mines(self,sentence):
        if sentence.count==0:
            for i in sentence.cells:
                self.mark_safe(i)
            return True
        return False

    def inferred(self,new_sentence):
        for sentence in self.knowledge:
            if new_sentence.cells < sentence.cells:
                s=copy.deepcopy(sentence)
                #s=Sentence(sentence.cells,sentence.count)#
                #s.cells=s.cells.union(sentence.cells)
                s.cells=s.cells.difference(new_sentence.cells)
                s.count-=new_sentence.count
                self.knowledge_append(s)
            elif sentence.cells<new_sentence.cells:
                s=copy.deepcopy(new_sentence)
                #s=Sentence(new_sentence.cells,new_sentence.count)#.cells.union(sentence.cells)
                #s.cells=s.cells.union(new_sentence.cells)
                s.cells=s.cells.difference(sentence.cells)
                s.count-=sentence.count
                self.knowledge_append(s)

    def knowledge_append(self,new_sentence):
        if self.all_mine(new_sentence):
            self.knowledge_known_mines()
        elif self.no_mines(new_sentence):
            self.knowledge_known_safes()#new_sentence)
        else:
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)
                self.inferred(new_sentence)

    def knowledge_known_mines(self):
        for i in self.knowledge:
            i.known_mines()

    def knowledge_known_safes(self):
        for i in self.knowledge:
            i.known_safes()
