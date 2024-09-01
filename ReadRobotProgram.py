def getAllStatementsInRoutine(scope, statements=None):
	'''Returns a list of all statements in a given routine or scope'''
	if not statements:
		statements = []
	
	for statement in scope.Statements:
		statements.append(statement)
		if statement.Scopes:
			for scope in statement.Scopes:
				getAllStatementsInRoutine(scope, statements)

	return statements
  
def getAllStatementsInRobotProgram(program, includeAllRoutines=True, limitCallToSubroutine=True):
	'''Returns a list of all statements in robot program.
	The optional includeAllRoutines parameter has a default value of True.
	You can pass a False value to only include statements from called subroutines and exclude statements from unused subroutines.
	The optional limitCallToSubroutine parameter has a default value of True and can be used with the includeAllRoutines parameter.
	Use caution since there may be multiple calls to the same subroutine.
	You can pass a False value to not exclude statements from a subroutine that have already been added to list.
	'''
	statements = getAllStatementsInRoutine(program.MainRoutine)
  
	#will only include statements from called subroutines
	if includeAllRoutines == False:
		searchedSubroutines = []
		
		for statement in statements:
			subroutine = statement.getProperty("Routine")
			if subroutine and subroutine.Value:
				#test whether to limit additional call to subroutine
				if limitCallToSubroutine == True and subroutine.Value in searchedSubroutines:
					continue
				else:
					statements.extend(getAllStatementsInRoutine(subroutine.Value))
					searchedSubroutines.append(subroutine.Value)

	#will include statements from all subroutines
	elif includeAllRoutines == True:
		for subroutine in program.Routines:
			statements.extend(getAllStatementsInRoutine(subroutine))

	return statements

def getAllPositionsInRoutine(scope):
	'''Returns a list of all positions used by motion statements in a routine or scope'''
	statements = getAllStatementsInRoutine(scope)
	positions = []
	for statement in statements:
		try:
			for position in statement.Positions:
				positions.append(position)
		except:
			pass
      
	return positions

  
def getAllPositionsInRobotProgram(program):
	'''Returns a list of all positions used by all motion statements in robot program.'''
	positions = getAllPositionsInRoutine(program.MainRoutine)
  
	for subroutine in program.Routines:
		positions.extend(getAllPositionsInRoutine(subroutine));

	return positions