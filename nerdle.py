from itertools import permutations


def check_permutation(perm, operators):
	"""
	Two main actions being performed:

		1. Check if permutation is valid. Not valid if any of the below is true:
			- First or last character is an operator
			- There are two operators in a row
			- There are no operators in the permutation

		2. If the permutation is valid, sequentially place a '==' in each position to
			create different equation versions within the same permutation.
	"""
	potential_equations_list = []
	valid_perm = True

	# invalidate this permutation if first or last character is an operator
	if perm[0] in operators or perm[-1] in operators:
		valid_perm = False

	if valid_perm:

		is_operator_list = []
		x = 0

		while (x <= len(perm)-1) and valid_perm:
			
			# check whether the element is an operator
			is_operator = perm[x] in operators

			# track whether each element in the list is an operator
			is_operator_list.append(is_operator)

			# If there are 2 operators in a row, fail the check because cannot be a valid equation.
			# Since we are looking backwards one element, check can only be performed when x > 0
			if x > 0 and is_operator_list[x-1] and is_operator_list[x]:
				valid_perm = False

			# If still valid, insert an '==' sign at each sequential position, but only if would not be immediately
			#  preceded by or followed by an operator.
			# Note that cannot insert '==' at the first position, hence checking that x > 0
			if valid_perm and x > 0 and (not perm[x-1] in operators) and (not perm[x] in operators):
				perm_copy = perm.copy()
				perm_copy.insert(x, '==')
				potential_equation = ''.join(perm_copy)
				potential_equations_list.append(potential_equation)

			x += 1

		# finally, make sure there is at least one operator in the permutation
		if not any(is_operator_list):
			valid_perm = False

	if valid_perm:
		return potential_equations_list
	else:
		return []


def validate_equations(potential_equations_list):
	"""
	For the list of potentially valid equation, check whether they evaluate to TRUE
	"""
	passed_equations_list = []
	result = False

	for equation in potential_equations_list:

		try:
			result = eval(equation)
			if result:
				passed_equations_list.append(equation)
		except:
			pass

	return passed_equations_list


def get_valid_equations(equation_length):
	"""
	Steps to get list of valid equations:
		1. Get all possible permutations
		2a. Check that the permutation is valid
		2b. Create different versions of the permutation by inserting "==" sign in different positions
		3. Evaluate each potential equation to see if TRUE (e.g. 2+2==4 is TRUE, 2+2==5 is FALSE)
	"""
	numbers = '0123456789'
	operators = '+-*/'
	chars = numbers + operators

	perms_list = list(permutations(chars, equation_length))
	
	valid_equations = []

	for perm in perms_list:

		# convert from tuple to list
		perm = list(perm)

		# iterate through this permutation to check for potentially valid equations
		potential_equations_list = check_permutation(perm, operators)
		
		# filter the potential equations to only those that are valid
		if potential_equations_list:
			passed_equations_list = validate_equations(potential_equations_list)
		
			# track the complete list of valid equations
			if passed_equations_list:
				valid_equations.extend(passed_equations_list)

	return valid_equations


def find_combinations(equations_list, equation_length):
	"""
	From the list of valid equations, check every unqiue pair
	Only return those that have fully unique characters, defined as (equation_length * 2) + 1 to account for the equals sign characters
	Note that the two separate "==" characters (one in each equation) get reduced to a single "=" in the set() operation
	"""
	first_equation = ""
	second_equation = ""
	combo_list = []

	for x in range(len(equations_list)):

		for y in range(x + 1, len(equations_list)):

			first_equation = equations_list[x]
			second_equation = equations_list[y]
			total_chars = len(list(set(first_equation + second_equation)))

			if total_chars == (equation_length * 2) + 1:
				combo_list.append(tuple((first_equation, second_equation)))

	return combo_list


def main():
	
	equation_length = 7
	valid_equations_list = get_valid_equations(equation_length)
	combo_list = find_combinations(valid_equations_list, equation_length)
	
	# print the first 10 results
	x = 0
	while x <= 9:
		print(combo_list[x])
		x += 1


if __name__ == '__main__':
	
	main()