
def try_parse(value, type, default=None):
	try:
		return type(value)
	except ValueError:
		return default

def int_try_parse(value, default=0):
	return try_parse(value, int, default)

def parse_query_string(dict, key, func, default=None):
	if key in dict:
		return func(dict[key], default)
	else:
		return default

def create_pagination(total_count, number_to_skip, page_size, page_number):
	pagination = { 'next' : False, 'previous' : False, 'previous_page_number' : page_number-1, 'next_page_number' : page_number+1}

	if (total_count - (number_to_skip+page_size)) > 0:
		pagination['next'] = True
	
	if number_to_skip > 0:
		pagination['previous'] = True

	return pagination