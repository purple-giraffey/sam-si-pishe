def flatten(list_of_lists):
    '''
    Takes a list of lists and returns a single list.
    '''
    return [y for x in list_of_lists for y in x]

