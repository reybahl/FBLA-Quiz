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
    for x in questions:
        if x['type'] == 'fillblank' or x['type'] == 'true_false' or x['type'] == 'mult_choice':
            pass   
        elif x['type'] == 'checkbox':
            pass
# x= dict([('education', '0'), (' service', '1'), (' leadership', '2'), ('Question1', '0'), ('Question1', 'True'), ('Answer1', 'fasdf')])

print(convert_to_dict([('checkbox', '0'), ('checkbox', '1'), (' leadership', '2'), ('Question1', '0'), ('Question1', 'True'), ('Answer1', 'fasdf')]))