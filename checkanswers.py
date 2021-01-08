from databaseconnect import Connection
connection = Connection()

def convert_to_dict(_list):
    d = {}
    matching_dict = {}
    for a, b in _list:
        if b == 'checkbox':
            d.setdefault(b, []).append(a)
        elif "matching" in a:
            matching_dict[a.replace('matching_','')] = b
        else:
            d.setdefault(a, []).append(b)
    d['matching'] = matching_dict
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
        
        elif x['type'] == 'matching':
            answer = question['answer']
            response = responses['matching']
            shared_items = {k: answer[k] for k in answer if k in response and answer[k] == response[k]}
            boolcorrect = len(shared_items) == len(answer)
            results.append({'type': x['type'], 
            'question': question['content'],
            'answer': response,
            'correct' : answer,
            'boolcorrect' : boolcorrect})

    score = 0
    for result in results:
        if result['boolcorrect']: #if the answer is correct
            score += 1 #add one to the score

    return results, score