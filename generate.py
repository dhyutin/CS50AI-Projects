import sys
from crossword import *
import copy


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        domain = copy.deepcopy(self.domains)

        for var in domain:
            l = var.length

            for word in domain[var]:
                if l != len(word):
                    # remove word
                    self.domains[var].remove(word)
        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        revised = False

        x_overlap = self.crossword.overlaps[x, y][0]
        y_overlap = self.crossword.overlaps[x, y][1]

        domain = copy.deepcopy(self.domains)

        if x_overlap != None:
            for ex in domain[x]:
                # check if any y satisfies constrains for x, y
                flag = 0
                for why in domain[y]:
                    if ex[x_overlap] == why[y_overlap]:
                        flag = 1
                        break

                if flag == 1:
                    continue
                else:
                    self.domains[x].remove(ex)
                    revised = True
        return revised
        # raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            # queue
            q = []
            # Load with all arcs in csp
            for var in self.domains:
                for var1 in self.crossword.neighbors(var):
                    if self.crossword.overlaps[var, var1] != None:
                        q.append((var, var1))
        
        while(len(q) > 0):
            x = q[0][0]
            y = q[0][1]
            q.pop(0)

            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        q.append((z, x))
            
            return True
        # raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            if var not in assignment:
                return False
        
        return True
        # raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        words = [*assignment.values()]
        if(len(words) != len(set(words))):
            return False
        
        for var in assignment:
            if var.length != len(assignment[var]):
                return False

        for var in assignment:
            for nn in self.crossword.neighbors(var):
                if nn in assignment:
                    x, y = self.crossword.overlaps[var, nn]
                    if assignment[var][x] != assignment[nn][y]:
                        return False       
        return True
        # raise NotImplementedError

    def order_domain_values(self, var, assignment):
        d = {}
        neighbours = self.crossword.neighbors(var)
        for word in self.domains[var]:
            i = 0
            for neighbour in neighbours:
                if neighbour not in assignment:
                    x_overlap = self.crossword.overlaps[var, neighbour][0]
                    y_overlap = self.crossword.overlaps[var, neighbour][1]
                    for neighbour_word in self.domains[neighbour]:
                        if word[x_overlap] != neighbour_word[y_overlap]:
                            i += 1
            d[word] = i
        sorted = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
        return [*sorted]
        # raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        choices = {}
        for variable in self.domains:
            if variable not in assignment:
                choices[variable] = self.domains[variable]
        sorted_ = [v for v, k in sorted(choices.items(), key=lambda item:len(item[1]))]
        return sorted_[0]
        # raise NotImplementedError

    def backtrack(self, assignment):
        if len(assignment) == len(self.domains):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            assignment1 = assignment.copy()
            assignment1[var] = value

            if self.consistent(assignment1):
                result = self.backtrack(assignment1)
                if result is not None:
                    return result
        return None        
        # raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
