from drkns.generation.pattern_util \
    import format_list_in_template, format_list_optional_in_template


def test_format_list_in_template():
    items = ('Je voudrais pas crever ' +
             '\nAvant d\'avoir connu' +
             '\nLes chiens noirs du Mexique').split(' ')
    template = '''
        An instant of poetry
        
 ## %WORDS{ }% ##
            
                Boris Vian
    '''
    formatted = format_list_in_template(
        'WORDS', items, template, line_level=False)
    assert('chiens noirs' in formatted)
    assert('Boris Vian' in formatted)
    assert ('##' in formatted)
    assert('WORDS' not in formatted)

    formatted = format_list_in_template(
        'WORDS', items, template, line_level=True)
    assert ('##' not in formatted)


def test_format_list_optional_in_template():
    template = '''
    
    ## %WORDS?{kapapi}% ##
    
    '''
    formatted = format_list_optional_in_template('WORDS', [], template)
    assert('kapapi' not in formatted)
    assert('WORDS' not in formatted)

    formatted = format_list_optional_in_template('WORDS', ['anything'], template)
    assert ('kapapi' in formatted)
    assert ('WORDS' not in formatted)
