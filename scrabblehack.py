import sys, getopt

def extract_by_size(size, dictionary):
	"""Extract words that are less than or equal to the given size"""
	print "Finding words with size less than or equal to '%s'" %(size)
	wordlist = []
	
	for word in dictionary:
		if len(word) <= int(size)+1: #had to do the +1 because len(word) counts the \n
			wordlist.append(word)

	return wordlist
	
def extract_by_letters(letters, dictionary):
	"""Extract words that contain the given (unordered) list of letters""" 
	print "Finding words with the letters '%s'" %(letters)
	
	wordlist = []
	flag = False
	
	for word in dictionary:
		flag = True
		for letter in letters:
			if letters.count(letter) != word.count(letter):
				flag = False
				break
		if flag == True:
			wordlist.append(word)
				
	return wordlist
		
def extract_by_word_segment(word_seg, dictionary):
	"""Extract words that contain the given word segment"""
	print "Finding words that contain the word '%s'" %(word_seg)
	wordlist = []
	
	for word in dictionary:
		if word_seg in word:
			wordlist.append(word)
			
	return wordlist
	
def error():
	print 'Usage: scrabblehack -f [FILE] [OPTIONS]'
	print "Try 'scrabblehack --help' for more information"
	
def usage():
	print 'Usage: scrabblehack -f [FILE] [OPTIONS]'
	print 'The dictionary must be a plaintext file of words separated by linebreaks.\n'
	print 'File options:'
	print '\t-f [FILE]\tinput dictionary REQUIRED'
	print '\t-o [FILE]\toutput file (optional, will print to stdout \n\t\t\tif output file is not specified) \n\t\t\tNOTE: will overwrite existing file of the same name\n'
	print 'Accepted first-letter parameters:'
	print '\t-u\t\tLowercase first-letters will be included in the search \n\t\t\t(this is default unless another accepted-letter \n\t\t\tparameter is specified)'
	print '\t-U\t\tUppercase first-letters will be included in the search \n\t\t\t(if this is specified, and -u is not, \n\t\t\tlowercase letters will be excluded)'
	print '\t-n\t\tNumbers will be included (why?)\n'
	print 'Filter options:'
	print '\t-l [LETTERS]\tsearches for words that contain the specified \n\t\t\tstring of letters (unordered)\n\t\t\tNote: if you include only one of a specified letter,\n\t\t\tscrabblehack will only extract words with one \n\t\t\tof that letter'
	print '\t-w [WORD SEG]\tsearches for words that contain the specified \n\t\t\tword segment'
	print '\t-s [SIZE]\tsearches for words of size less than or equal to \n\t\t\t[SIZE]\n'
	print 'Other options:'
	print '\t-h, --help\tview this help file'
		
########################Main!
def main(argv):
	"""A scrabble program for finding words based on word segments, sets of letters, and max sizes"""
	lowercase = 'abcdefghijklmnopqrstuvwxyz'
	uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	numbers = '0123456789'
	accepted_letters = []
	write_flag = False
	size_flag = False
	letters_flag = False
	word_seg_flag = False
	lc_flag = False
	uc_flag = False
	num_flag = False
	
	try:
		opts, args = getopt.getopt(argv, 'f:o:l:w:s:uUnh', ["help", "awesome"])
	except getopt.GetoptError:
		error()
		sys.exit(2)
		
	if opts == []:
		error()
		sys.exit(2)
		
	for opt, arg in opts:
		if opt in ['-h', '--help']:
			usage()
			sys.exit()
		if opt == '--awesome':
			print 'THIS IS THE COOLEST LINE OF CODE I HAVE EVER WRITTEN:\ndictionary = [word for word in dictionary if word[0] in accepted_letters]'
			sys.exit()
		
	if '-f' not in opts[0]:
		print 'Need a dictionary'
		error()
		sys.exit() 
		
	#if no accepted-letter parameters passed, default to lowercase
	#couldn't seem to string the ifs together...
	if ('-u', '') not in opts:
		if ('-n', '') not in opts:
			if('-U', '') not in opts:
				print 'No accepted-letter parameters given, defaulting to lowercase only.'
				accepted_letters.extend(lowercase)
		
	for opt, arg in opts:
		if opt == '-f':
			try:
				dict_file = open(arg)
				dictionary = list(dict_file)
				dict_file.close()
				print 'Working...'
			except:
				print 'Invalid dictionary'
				error()
				sys.exit()
		elif opt == '-u':
			lc_flag = True
		elif opt == '-U':
			uc_flag = True
		elif opt == '-n':
			num_flag = True
		elif opt == '-l':
			letters_flag = True
			letters = arg
		elif opt == '-w':
			word_seg_flag = True
			word_seg = arg
		elif opt == '-s':
			size_flag = True
			size = arg
		elif opt == '-o':
			filename = arg
			write_flag = True
		else:
			error()
			sys.exit()
			
	#using flags instead of doing the processing in the ifs allows me to do the processing
	#independent of the order that the user gave
			
	if lc_flag is True:
		accepted_letters.extend(lowercase)
		
	if uc_flag is True:
		accepted_letters.extend(uppercase)
	
	if num_flag is True:
		accepted_letters.extend(numbers)
		
	#filter out all the words that don't match the accepted_letters parameters
	#THIS IS THE COOLEST LINE OF CODE I HAVE EVER WRITTEN
	dictionary = [word for word in dictionary if word[0] in accepted_letters]
	
	if word_seg_flag is True:
		dictionary = extract_by_word_segment(word_seg, dictionary)
	
	if size_flag is True:
		dictionary = extract_by_size(size, dictionary)
		
	if letters_flag is True:
		dictionary = extract_by_letters(letters, dictionary)
			
	if write_flag is False:
		for word in dictionary: sys.stdout.write(word)
		print 'No output file specified, so I printed to stdout'
	else:
		stdout_default = sys.stdout
		output = open(filename, 'w')
		sys.stdout = output
		for word in dictionary:
			sys.stdout.write(word)
		sys.stdout = stdout_default
		num_words = len(dictionary)
		print "List of %d words saved to '%s'" % (num_words, filename)
		sys.exit()
		
		
	
if __name__ == '__main__': main(sys.argv[1:])	
		
		
