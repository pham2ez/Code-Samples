import sys
sys.setrecursionlimit(10000)
import random


class HyperMinesGame:
    def __init__(self, dims, bombs):
        """Start a new game.

        This method should properly initialize the "board", "mask",
        "dimensions", and "state" attributes.

        dims (list): Dimensions of the board
        bombs (list): Bomb locations as a list of lists, each an
                         N-dimensional coordinate
        """
        # sets a blank template to work with
        self.dimensions = dims
        self.state = "ongoing"
        self.mask = self.NDarray(False, 0)
        self.board = self.NDarray(0, 0)

        # sets the bombs through given list/tuple
        for i in bombs:
            self.change(i, '.', self.board, 0)

        # counts number of bombs surrounding a non-bomb tile and also makes the changes internal
        self.NDall(self.board, [])

    def dig(self, coords):
        """Recursively dig up square at coords and neighboring squares.

        Update the mask to reveal square at coords; then recursively reveal its
        neighbors, as long as coords does not contain and is not adjacent to a
        bomb.  Return a number indicating how many squares were revealed.  No
        action should be taken and 0 returned if the incoming state of the game
        is not "ongoing".

        The updated state is "defeat" when at least one bomb is visible on the
        board after digging, "victory" when all safe squares (squares that do
        not contain a bomb) and no bombs are visible, and "ongoing" otherwise.

        coords (list): Where to start digging

        Returns:
           int: number of squares revealed
        """
        # checks current states and chosen tile before searching within the board
        if self.state == "defeat" or self.state == "victory":
            return 0

        if self.look(coords, self.board, 0) == '.':
            self.change(coords, True, self.mask, 0)
            self.state = "defeat"
            return 1

        # legally uncovers all neighbors and counts along the way of uncovering
        count = self.blanks(coords)

        # see if all non-bomb tiles are all uncovered, if not continue game
        covered_squares = self.counting(self.mask, [])
        if covered_squares == 0:
            self.state = "victory"
            return count
        else:
            return count

    def render(self, xray=False):
        """Prepare the game for display.

        Returns an N-dimensional array (nested lists) of "_" (hidden squares),
        "." (bombs), " " (empty squares), or "1", "2", etc. (squares
        neighboring bombs).  The mask indicates which squares should be
        visible.  If xray is True (the default is False), the mask is ignored
        and all cells are shown.

        xray (bool): Whether to reveal all tiles or just the ones allowed by the mask

        Returns:
           An n-dimensional array (nested lists)
        """
        # creates new list (of lists) with string objects with/without hidden elements
        new = self.NDarray(0, 0)
        self.check(new, new, [], xray)
        return new

    # HELPER FUNCTIONS
    def blanks(self, dims):
        """Recurses through blank/0 tiles in order to uncover all connecting blank/0
            tiles and stopping when showing nearby numbered tiles. Also while doing
            this returns back the amount of tiles uncovered.

            """
        count = 0
        # if chosen tile has not been already uncovered, sets it to true since we are uncovering it and adding that to the rest of what we have previously uncovered as well
        if self.look(dims, self.mask, 0) == False:
            self.change(dims, True, self.mask, 0)
            count += 1

        # looks to see if the tile we just uncovered was a 0 tile first and then searches neighbors, if numbered tile, just return count
        if self.look(dims, self.board, 0) == 0:
            neighborsList = self.NDneighbors(dims, 0)
            for neighbor in neighborsList:
                if self.look(neighbor, self.mask, 0) == False:
                    if self.look(neighbor, self.board, 0) == 0:
                        count += self.blanks(neighbor)
                    elif self.look(neighbor, self.board, 0) != '.':
                        self.change(neighbor, True, self.mask, 0)
                        count += 1
        return count

    def counting(self, current, dims):
        """Counts and then returns the number of tiles left to uncover aka covered non-bomb tiles.

            current (list) = the current list we are looking at, either mask/board
            dims (list) = list that we keep track of what location we are in for self.look function

            """
        count = 0
        # looks through the entire board's mask
        for i in range(len(current)):
            # reached the furthest depth
            if type(current[i]) == bool:
                dims.append(i)
                # this counts the number of covered non-bombs
                if current[i] == False and self.look(dims, self.board, 0) != '.':
                    count += 1
                dims.pop(len(dims) - 1)
            else:
                dims.append(i)
                count += self.counting(current[i], dims)
                dims.pop(len(dims) - 1)
        return count

    def check(self, into, current, dims, xray):
        """Does the rendering based off of what self.board is and changes the new array to have the string values of board as necessary for xray.

            into (list) = our initial array that we are altering
            current (list) = the current list we are looking at, either mask/board
            dims (list) = list that we keep track of what location we are in for self.look function
            xray (bool) = if we are showing all of them or only when the mask is true

        """
        # goes through the entire board to return string values appropriate to xray
        for i in range(len(current)):
            # reached the furthest depth
            if type(current[i]) == int:
                dims.append(i)
                mask = self.look(dims, self.mask, 0)
                value = self.look(dims, self.board, 0)
                # this is where string values of board are added
                if xray == False and mask == False:
                    self.change(dims, '_', into, 0)
                elif value == 0:
                    self.change(dims, ' ', into, 0)
                else:
                    self.change(dims, str(value), into, 0)
                dims.pop(len(dims) - 1)
            else:
                dims.append(i)
                self.check(into, current[i], dims, xray)
                dims.pop(len(dims) - 1)

    def NDarray(self, value, depth):
        """Creates a new ND array with the initial value that we want the new entire array to have.

            value (int/str) = the initial value we want
            depth (int) = how deep in we are

        """
        # checks to see if we have finally reached the 1D dimension of our array and then returns that 1D array
        if depth == len(self.dimensions) - 1:
            array = []
            for i in range(self.dimensions[depth]):
                array.append(value)
            return array

        # set up for making the array the right size after getting the 1D dimension
        else:
            array = []
            for i in range(self.dimensions[depth]):
                array.append(self.NDarray(value, depth + 1))
            return array

    def NDall(self, current, dims):
        """Looks through all of the values and checks the number of bombs around each initial 0 tile and then changes that tile if needed

            current (list) = current list we're looking at, either mask/board
            dims (list) = the neighbors of this coordinate

        """
        # looks through the entire array
        for i in range(len(current)):
            # reached the furthest depth
            if type(current[i]) == str or type(current[i]) == int:
                if current[i] == 0:
                    dims.append(i)
                    count = 0
                    # find neighbors and then counts how many bomb neighbors
                    check = self.NDneighbors(dims, 0)
                    for poss in check:
                        if self.look(poss, self.board, 0) == '.':
                            count += 1
                    self.change(dims, count, self.board, 0)
                    dims.pop(len(dims) - 1)
            else:
                dims.append(i)
                self.NDall(current[i], dims)
                dims.pop(len(dims) - 1)

    def NDneighbors(self, dims, depth):
        """Returns a list of all of the neighbors based off of the coordinates first given, should give 3*len(dims) neighbors

            dims (list) = the neighbors of this coordinate
            depth (int) = how deep in we are
        """

        total_neighbors = []
        # base case returns back a list of (current dimension-1, current dimension +1)
        if depth == len(dims) - 1:
            ret = []
            for i in range(dims[depth] - 1, dims[depth] + 2):
                if i > -1 and i < self.dimensions[depth]:
                    ret.append([i])
            return ret
        # add the different neighbors separately so they can be checked with look or change
        else:
            for i in range(dims[depth] - 1, dims[depth] + 2):
                if i > -1 and i < self.dimensions[depth]:
                    if len(dims) > 1:
                        temp = self.NDneighbors(dims, depth + 1)
                        for a in temp:
                            if type(a) == list:
                                new = [i]
                                new.extend(a)
                                total_neighbors.append(new)
                            else:
                                total_neighbors.append([i, a])
        return total_neighbors

    def change(self, location, value, current, depth):
        """Changes the value at that specific coordinate in an array

            location (list) = where we want to change the value
            value (int/str) = what we want to change the current value to
            current (list) = current list we're looking at, either mask/board
            depth (int) = how deep in we are
        """
        # reaches the depth necessary and then changes the value there
        if depth == len(self.dimensions) - 1:
            current[location[depth]] = value
        else:
            self.change(location, value, current[location[depth]], depth + 1)

    def look(self, location, current, depth):
        """Returns the value at that specific coordinate in an array

            location (list) = where we want to be looking at
            current (list) = current list we're looking at, either mask/board
            depth (int) = how deep in we are
        """
        # reaches the depth necessary and then returns the value there
        if depth == len(self.dimensions) - 1:
            return current[location[depth]]
        else:
            return self.look(location, current[location[depth]], depth + 1)

    def helper_print(self, current):
        """"Helps to read recursively"""
        # reached the furthest depth
        # looks through the entire array
        out = ""
        for i in range(len(current)):
            # reached the furthest depth
            if type(current[i]) == str:
                for i in current:
                    out += i
                return out
            else:
                out += self.helper_print(current[i])
                if i != len(current)-1:
                    out += "\n"
        return out

    def render_ascii(self, xray = False):
        """Prints out render in a more readable fashion"""
        show = self.render(xray)
        out = "begin \n"
        out += self.helper_print( show)
        out += "end \n"
        return out

if __name__ == '__main__':

    play = True
    while play:

        x, y = input("What size game do you want? (e.g. 4 5 for a 4 by 5 minesweeper board): ").split()
        x = int(x)
        y = int(y)
        bombs = []
        for i in range(min(int(x / 2)+1, (y / 2)+1)):
            bombx = random.randint(0, x - 1)
            bomby = random.randint(0, y - 1)
            bombs.append([bombx, bomby])

        g = HyperMinesGame([x, y], bombs)
        for i in range(g.dimensions[0]*g.dimensions[1]-len(bombs)):
            print(g.render_ascii(False))
            x, y = input("Now where would you like to dig? (e.g. 4 5 to dig at the 4th row and 5th column): ").split()
            g.dig([int(x)-1,int(y)-1])
            if g.state == "victory":
                print(g.render_ascii(True))
                cont = input("You won! Would you like to try again? (Y/N): ")
                if cont == "N" or cont == "n":
                    play = False
                    break
                elif cont == "Y" or cont == "y":
                    break
                else:
                    print("You gave me an invalid response, so you don't get to play anymore!")
                    break
            elif g.state == "defeat":
                print(g.render_ascii(True))
                cont = input("Better luck next time! Would you like to redeem yourself? (Y/N): ")
                if cont == "N" or cont == "n":
                    play = False
                    break
                elif cont == "Y" or cont == "y":
                    break
                else:
                    print("You gave me an invalid response, so you don't get to play anymore!")
                    break






