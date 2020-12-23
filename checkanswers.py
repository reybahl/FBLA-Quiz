from databaseconnect import Connection
connection = Connection()

def convert_to_dict(_list):
    d = {}
    for a, b in _list:
        if b == 'checkbox':
            d.setdefault(b, []).append(a)
        else:
            d.setdefault(a, []).append(b)
    return d

def check(questions, responses):
    responses = convert_to_dict(responses)
    print(responses)
    results = []
    for x in questions:
        if x['type'] == 'fillblank':
            results.append({'type': x['type'], 
            'question': x['name'], 
            'answer': responses['fillblank'][0], 
            'correct' : x['answer'], 
            'boolcorrect' : responses[x['type']][0] == x['answer']})    
        elif x['type'] == 'checkbox':
            for correct_choice in x['answer']:
                correct_choice.replace(' ', '')
            for selected in responses['checkbox']:
                selected.replace(' ', '')

            correct = sorted(x['answer']) if type(x['answer']) == 'list' else x['answer']
            if len(responses['checkbox']) == 1:
                response = responses['checkbox'][0] 
            else:
                response = sorted(responses['checkbox'])
            results.append({'type': x['type'], 
            'question': x['name'], 
            'answer': response, 
            'correct' : correct_choice, 
            'boolcorrect' : bool(response == correct_choice)})
        elif x['type'] == 'mult_choice' or x['type'] == 'true_false':
            results.append({'type': x['type'], 
            'question': x['name'], 
            'answer': responses[x['type']][0], 
            'correct' : x['answer'], 
            'boolcorrect' : responses[x['type']][0].lower() == x['answer'].lower()})
        

    print(results)
    return results


#print(convert_to_dict([('checkbox', '0'), ('checkbox', '1'), (' leadership', '2'), ('Question1', '0'), ('Question1', 'True'), ('Answer1', 'fasdf')]))