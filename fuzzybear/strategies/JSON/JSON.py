from .. import Strategy
import json
import random
from random import randint
import copy

# config
MAX_KEYS = 50
MAX_ENTRIES = 100
ITERATION_MAX = 100


def insert(key,value,json_obj):
    """ insert a key value pair """
    json_obj[key] = value


def replace_val(find,replace,json_obj):
    """ given a value replace it """
    for item in json_obj.items():
        if item[1] == find:
            #print(item)
            json_obj[item[0]] = replace
            

def random_entry(json_obj):
    """ random entry within dictionary """
    itt = list(json_obj.items())
    entry = random.choice(itt)
    return entry


def get_rand_field(json_obj):
    """ select a random field in the JSON obj """
    return random.choice(list(json_obj.items()))


def thicc_file(num_entries):
    """ add extra JSON fields in a range """
    thiccboi = {}
    for i in range(num_entries):
        thiccboi[i] = []

        for l in range(1, MAX_KEYS):
            thiccboi[i].append(l)

    return thiccboi


class JSON(Strategy.Strategy):
    
    def __init__(self, sample_input):
        """ parse JSON input """
        super()
        self.sample_input = sample_input
        with open(sample_input) as jsonfile:
            self.candidate_input = json.load(jsonfile)
        self.size = len(self.candidate_input)


    def run(self):
        """ run the JSON generator """
        rand_entry_count = randint(1, MAX_ENTRIES)
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
        for field in range(ITERATION_MAX):
            mutation = copy.deepcopy(self.candidate_input)
            rand_field = get_rand_field(mutation)

            field_value = rand_field[1] if (type(rand_field) is not list) else rand_field[1][0]
            negated = super().negate(field_value)
            
            if (type(rand_field[1]) is list): 
                mutation[rand_field[1][0]] = negated
            else:
                mutation[rand_field[0]] = negated

            yield json.dumps(mutation)

        # replace random fields with format strings
        for field in range(ITERATION_MAX):
            mutation = copy.deepcopy(self.candidate_input)
            rand_field = get_rand_field(mutation)
            for fmtstring in super().format_strings():
                field_value = rand_field[0] if (type(rand_field) is not list) else rand_field[1][0]
                mutation[field_value] = fmtstring
                yield json.dumps(mutation)

        # replace random fields with system paths
        for field in range(ITERATION_MAX):
            mutation = copy.deepcopy(self.candidate_input)
            rand_field = get_rand_field(mutation)
            for path in super().system_paths():
                field_value = rand_field[0] if (type(rand_field) is not list) else rand_field[1][0]
                mutation[field_value] = path

                yield json.dumps(mutation)

        # replace random fields with polyglots
        for field in range(ITERATION_MAX):
            mutation = copy.deepcopy(self.candidate_input)
            rand_field = get_rand_field(mutation)
            for polyglot in super().polyglots():
                field_value = rand_field[0] if (type(rand_field) is not list) else rand_field[1][0]
                mutation[field_value] = polyglot
                yield json.dumps(mutation)

        # replace random fields with max constants
        for field in range(ITERATION_MAX):
            mutation = copy.deepcopy(self.candidate_input)
            rand_field = get_rand_field(mutation)
            for constant in super().max_constants():
                field_value = rand_field[0] if (type(rand_field) is not list) else rand_field[1][0]
                mutation[field_value] = constant
                yield json.dumps(mutation)

        # replace random fields with byte flips
        for field in range(ITERATION_MAX):
            mutation = copy.deepcopy(self.candidate_input)
            rand_field = get_rand_field(mutation)
            field_value = rand_field[0] if (type(rand_field) is not list) else rand_field[1][0]
            mutation[field_value] = super().byte_flip(field_value)
            yield json.dumps(mutation)


"""devnotes

-> Some of the code above is truly fucking magical
    -> like how does a tuple become mutable
    -> we got list magic its all happening

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
"""