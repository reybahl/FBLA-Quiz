from databaseconnect import Connection
connection = Connection()

def convert_to_dict(_list):
    d = {}
    for a, b in _list:
        if b == 'checked':
            d.setdefault(b, []).append(a)
        else:
            d.setdefault(a, []).append(b)
    return d

def check(questions, responses):
    responses = convert_to_dict(responses)
    #print(responses)
    results = []
    
    for x in questions:
        question = x['question']
        if x['type'] == 'fill_in_the_blank':
            results.append({'type': x['type'], 
            'question': question['content'],
            'answer': responses['fill_in_the_blank'][0],
            'correct' : question['answer'],
            'boolcorrect' : responses[x['type']][0] in question['answer']})
        
        elif x['type'] == 'checkbox':

            correct = sorted(question['answer'])

            response = sorted(responses['checkbox'])

            results.append({'type': x['type'], 
            'question': question['content'],
            'answer': response, 
            'correct' : correct,
            'boolcorrect' : response == correct})

        elif x['type'] == 'multiple_choice' or x['type'] == 'true_false':
            if type(question['answer']) == 'list':
                correct_fixed = [choice.lower() for choice in question['answer']]
                boolcorrect = responses[x['type']][0].lower() in correct_fixed
            elif type(question['answer'] == 'str'):
                correct_fixed = question['answer'].lower()
                boolcorrect = responses[x['type']][0].lower() == correct_fixed
            results.append({'type': x['type'], 
            'question': question['content'],
            'answer': responses[x['type']][0], 
            'correct' : correct_fixed,
            'boolcorrect' : boolcorrect})
        

    print(results)
    return results


#print(convert_to_dict([('checkbox', '0'), ('checkbox', '1'), (' leadership', '2'), ('Question1', '0'), ('Question1', 'True'), ('Answer1', 'fasdf')]))