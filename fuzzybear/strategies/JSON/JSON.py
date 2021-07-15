from .. import Strategy
import json
import random
from random import randint
import copy


def insert(key,value,json_obj):
    json_obj[key] = value


#given a value replace it
def replace_val(find,replace,json_obj):
    for item in json_obj.items():
        if item[1] == find:
            #print(item)
            json_obj[item[0]] = replace
            

# random entry within dictionary
def random_entry(json_obj):
    itt = list(json_obj.items())
    entry = random.choice(itt)
    return entry


def get_rand_field(json_obj):
    return random.choice(list(json_obj.items()))


def thicc_file(num_entries):
    thiccboi = {}
    for i in range(0,num_entries):
        thiccboi[i] = []

        for l in range(1,50):
            thiccboi[i].append(l)

    return thiccboi


class JSON(Strategy.Strategy):
    
    # parse csv input data
    def __init__(self, sample_input):
        super()
        self.sample_input = sample_input
        with open(sample_input) as jsonfile:
            self.candidate_input = json.load(jsonfile)
        
        self.size = len(self.candidate_input)


    # run strategies
    def run(self):

        rand_entry_count = randint(1, 100)
        mutation = thicc_file(rand_entry_count)
        yield json.dumps(mutation)
        
        # Replace random key with chonky value
        mutation = copy.deepcopy(self.candidate_input)
        rand_key = random_entry(mutation)
        for chonk in super().chonk():
            if (type(rand_key[1]) is list): 
                rand_key[1][0] = chonk
            else:
                mutation[rand_key[0]] = chonk

            yield json.dumps(mutation)

        # negate random fields
        mutation = copy.deepcopy(self.candidate_input)
        rand_field = get_rand_field(mutation)

        field_value = rand_field[1] if (type(rand_field) is not list) else rand_field[1][0]
        # print(f'   [DEBUG] Selected random field {rand_field}')
        for negated in super().negate(field_value):
            if (type(rand_field[1]) is list): 
                rand_field[1][0] = negated
            else:
                mutation[rand_field[0]] = negated

            yield json.dumps(mutation)



'''devnotes

-> The json1 binary drops inputs if the length of the JSON is greater than 7200
-> Supplying a negative length field to the json1 binary segfaults it
-> Some of the code above is truly fucking magical
    -> like how does a tuple become mutable
    -> we got list magic its all happening
-> Owen says - "this is a crime against humanity" 

TODO

    - [X]  We probably need to run more tests against json bodies with vast nesting
           I have a feeling code blocks 65-70, 79-84 wont hold up

        * After testing with nesting.txt there is a good chance the code is fine
          the issue is that we cant get coverage of the json body itself because
          .items() will only deal with the outter layer of the object, it is not
          a recursive function. For example the json body,

        "complex1": {
            "key1": [12, 11],
            "key2": {
                "dearlord": ["a", "bb"]
            }
        },

        will not have internal fields like "key2" fuzzed since randfield will select,
            ('complex1', {'key1': [12, 11], 'key2': {'dearlord': ['a', 'bb']}}) 
        as a whole

    - [ ] Improve fuzzing of nested JSON bodies 
'''