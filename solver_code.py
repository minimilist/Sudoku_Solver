from typing import Tuple, List

def input_sudoku() -> List[List[int]]:
	"""Function to take input a sudoku from stdin and return
	it as a list of lists.
	Each row of sudoku is one line.
	"""
	sudoku= list()
	for _ in range(9):
		row = list(map(int, input().rstrip(" ").split(" ")))
		sudoku.append(row)
	return sudoku

def print_sudoku(sudoku:List[List[int]]) -> None:
	"""Helper function to print sudoku to stdout
	Each row of sudoku in one line.
	"""
	for i in range(9):
		for j in range(9):
			print(sudoku[i][j], end = " ")
		print()

# You have to implement the functions below

def get_block_num(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:
	"""This function takes a parameter position and returns
	the block number of the block which contains the position.
	"""
	if pos[1]%3 > 0:
		a = pos[1]//3 + 1
	else:
		a = pos[1]//3

	if pos[0]%3 > 0:
		b = 3*(pos[0]//3)
	else:
		b = 3*(pos[0]//3 - 1)
	return a + b

def get_position_inside_block(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:
	"""This function takes parameter position
	and returns the index of the position inside the corresponding block.
	"""
	b = get_block_num(sudoku,pos)
	if b%3 > 0:
		x = pos[1] - 3*(b%3 - 1)
	else:
		x = pos[1] - 6
	
	if pos[0]%3 > 0:
		y = pos[0] - 3*(b//3) - 1
	else:
		y = 2

	return x + 3*y


def get_block(sudoku:List[List[int]], x: int) -> List[int]:
	"""This function takes an integer argument x and then
	returns the x^th block of the Sudoku. Note that block indexing is
	from 1 to 9 and not 0-8.
	"""
	block = []
	for i in range(9):
		for j in range(9):
			if get_block_num(sudoku,(i+1,j+1)) == x:
				block.append(sudoku[i][j])
	return block
	

def get_row(sudoku:List[List[int]], i: int)-> List[int]:
	"""This function takes an integer argument i and then returns
	the ith row. Row indexing have been shown above.
	"""
	row = [ele for ele in sudoku[i-1]]
	return row

def get_column(sudoku:List[List[int]], x: int)-> List[int]:
	"""This function takes an integer argument i and then
	returns the ith column. Column indexing have been shown above.
	"""
	column = []
	for i in range(9):
		column.append(sudoku[i][x-1])
	return column

def find_first_unassigned_position(sudoku : List[List[int]]) -> Tuple[int, int]:
	"""This function returns the first empty position in the Sudoku. 
	If there are more than 1 position which is empty then position with lesser
	row number should be returned. If two empty positions have same row number then the position
	with less column number is to be returned. If the sudoku is completely filled then return `(-1, -1)`.
	"""
	empty = []
	for i in range(9):
		j = 0
		while j < 9:
			if sudoku[i][j] == 0:
				empty.append((i+1,j+1))
				j += 1
				break
			else:
				j += 1
				continue
		if j == 9:
			continue
		elif j < 9:
			break
	
	if empty == []:
		return (-1,-1)
	else:
		return empty[0]

def valid_list(lst: List[int])-> bool:
	"""This function takes a lists as an input and returns true if the given list is valid. 
	The list will be a single block , single row or single column only. 
	A valid list is defined as a list in which all non empty elements doesn't have a repeating element.
	"""
	for ele in lst:
		if ele != 0:
			if lst.count(ele) > 1:
				return False
	
	return True

def valid_sudoku(sudoku:List[List[int]])-> bool:
	"""This function returns True if the whole Sudoku is valid.
	"""
	for i in range(1,10):
		if valid_list(get_row(sudoku,i)) == False:
			return False
	for i in range(1,10):
		if valid_list(get_column(sudoku,i)) == False:
			return False
	for i in range(1,10):
		if valid_list(get_block(sudoku,i)) == False:
			return False
	return True


def get_candidates(sudoku:List[List[int]], pos:Tuple[int, int]) -> List[int]:
	"""This function takes position as argument and returns a list of all the possible values that 
	can be assigned at that position so that the sudoku remains valid at that instant.
	"""
	candidates = [1,2,3,4,5,6,7,8,9]
	for ele in get_row(sudoku,pos[0]):
		if candidates != []:
			if ele != 0:
				candidates.remove(ele)
	for ele in get_column(sudoku,pos[1]):
		if candidates != []:
			if ele != 0 and candidates.count(ele) > 0:
				candidates.remove(ele)
	for ele in get_block(sudoku,get_block_num(sudoku,pos)):
		if candidates != []:
			if ele != 0 and candidates.count(ele) > 0:
				candidates.remove(ele)
	return candidates

def make_move(sudoku:List[List[int]], pos:Tuple[int, int], num:int) -> List[List[int]]:
	"""This function fill `num` at position `pos` in the sudoku and then returns
	the modified sudoku.
	"""
	sudoku[pos[0]-1][pos[1]-1] = num
	return sudoku

def undo_move(sudoku:List[List[int]], pos:Tuple[int, int]):
	"""This function fills `0` at position `pos` in the sudoku and then returns
	the modified sudoku. In other words, it undoes any move that you 
	did on position `pos` in the sudoku.
	"""
	sudoku[pos[0]-1][pos[1]-1] = 0
	return sudoku

def sudoku_solver(sudoku: List[List[int]]) -> Tuple[bool, List[List[int]]]:
	""" This is the main Sudoku solver. This function solves the given incomplete Sudoku and returns 
	true as well as the solved sudoku if the Sudoku can be solved i.e. after filling all the empty positions the Sudoku remains valid.
	It return them in a tuple i.e. `(True, solved_sudoku)`.

	However, if the sudoku cannot be solved, it returns False and the same sudoku that given to solve i.e. `(False, original_sudoku)`
	"""
	if find_first_unassigned_position(sudoku) != (-1,-1):
		pos = find_first_unassigned_position(sudoku)
		ans = get_candidates(sudoku,pos)
		for ele in ans:
			sudoku = make_move(sudoku,pos,ele)
			(possible, sudoku) = sudoku_solver(sudoku)
			if possible:
				return(True, sudoku)
			else:
				sudoku = undo_move(sudoku,pos)
				continue

	else:
		return(True, sudoku)
	
	return (False, sudoku)


# Following is the driver code
if __name__ == "__main__":

	# Input the sudoku from stdin
	sudoku = input_sudoku()

	# Try to solve the sudoku
	possible, sudoku = sudoku_solver(sudoku)

	# Check if it could be solved
	if possible:
		print("Found a valid solution for the given sudoku :)")
		print_sudoku(sudoku)

	else:
		print("The given sudoku cannot be solved :(")
		print_sudoku(sudoku)
