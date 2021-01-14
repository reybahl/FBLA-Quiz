from databaseconnect import Connection

connection = Connection.Instance()


def convert_to_dict(responses):
    """Converts the users responses into a dictionary, 
    the format needed for checking

    :return: A formatted dictionary with the users responses organized by category
    """
    formatted_dict = {}
    matching_dict = {}
    for a, b in responses:
        if b == 'multiple_choice':
            formatted_dict.setdefault(b, []).append(a)
        elif "matching" in a:
            matching_dict[a.replace('matching_', '')] = b
        else:
            formatted_dict.setdefault(a, []).append(b)
    formatted_dict['matching'] = matching_dict

    return formatted_dict


def check(questions, responses):
    """Checks the user's responses based on the correct question and answer
    """
    responses = convert_to_dict(responses)
    results = [] #Results list

    for x in questions:
        question = x['question']
        if x['type'] == 'fill_in_the_blank': #Checking question type
            correct_answer = " or ".join(question['answer']) if type(question['answer']) == list else question['answer']
            lowered_correct_answer = [answer.lower() for answer in question['answer']] 
            results.append({'type': x['type'],
                            'question': question['content'],
                            'answer': responses['fill_in_the_blank'][0],
                            'correct': correct_answer,
                            'boolcorrect': responses[x['type']][0].lower() in lowered_correct_answer})

        elif x['type'] == 'multiple_choice':
            correct_answer = question['answer'] if type(question['answer']) == str else ", ".join(question['answer'])

            correct_sorted = sorted(question['answer']) if type(question['answer']) == list else question['answer'] #Sorts answer if it is a list

            correct_lowered = correct_sorted.lower() if type(correct_sorted) == str else [x.lower() for x in correct_sorted] #lowers all the answer choices

            response = ", ".join(responses['multiple_choice']) if type(responses['multiple_choice']) == list else responses['multiple_choice']

            response_sorted = sorted(responses['multiple_choice']) if len(responses['multiple_choice']) > 1 else responses['multiple_choice'][0]

            response_lowered = response_sorted.lower() if type(response_sorted) == str else [x.lower() for x in response_sorted]

            results.append({'type': x['type'],
                            'question': question['content'],
                            'answer': response,
                            'correct': correct_answer,
                            'boolcorrect': response_lowered == correct_lowered})

        elif x['type'] == 'dropdown' or x['type'] == 'true_false':
            correct_answer = question['answer']
            if type(question['answer']) == 'list':
                correct_fixed = [choice.lower() for choice in question['answer']]
                boolcorrect = responses[x['type']][0].lower() in correct_fixed
            elif type(question['answer'] == 'str'):
                correct_fixed = question['answer'].lower()
                boolcorrect = responses[x['type']][0].lower() == correct_fixed
            results.append({'type': x['type'],
                            'question': question['content'],
                            'answer': responses[x['type']][0],
                            'correct': correct_answer,
                            'boolcorrect': boolcorrect})

        elif x['type'] == 'matching':
            correct_answer = {k: question['answer'][k] for k in sorted(question['answer'])}
            response = {k: responses['matching'][k] for k in sorted(responses['matching'])}
            shared_items = {k: correct_answer[k] for k in correct_answer if k in response and correct_answer[k] == response[k]}
            boolcorrect = len(shared_items) == len(correct_answer)
            results.append({'type': x['type'],
                            'question': question['content'],
                            'answer': response,
                            'correct': correct_answer,
                            'boolcorrect': boolcorrect})

    score = 0
    for result in results:
        if result['boolcorrect']:  # if the answer is correct
            score += 1  # add one to the score

    return results, score