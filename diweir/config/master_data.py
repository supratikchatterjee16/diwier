import random

anonymization_map = {
    'empty' : {'desc' : 'Insert a NULL value', 'op' : lambda : None},
    'integer' : {'desc' : 'Insert an integer', 'op' : lambda a=10, b=0 : int(random.random() * 10 ** a) if b == 0 else round(random.random() * 10 ** a, b)},
    # 'string' : {'desc' : 'Insert a string', 'op' : lambda : None},
    'name' : {'desc' : 'Prepared full name', 'op' : lambda : None},
    'first-name' : {'desc' : 'First name', 'op' : lambda : None},
    'last-name' : {'desc' : 'Last name', 'op' : lambda : None},
    'isd' : {'desc' : 'International Dialing code', 'op' : lambda : None},
    'phone' : {'desc' : 'Phone Number', 'op' : lambda : None},
    'national-id' : {'desc' : 'National Identifier', 'op' : lambda : None},
    'card' : {'desc' : 'Credit/Debit Card Number', 'op' : lambda : None},
    'address' : {'desc' : 'Address', 'op' : lambda : None},
    'building' : {'desc' : 'Building Number', 'op' : lambda : None},
    'street' : {'desc' : 'Street', 'op' : lambda : None},
    'city' : {'desc' : 'City', 'op' : lambda : None},
    'province' : {'desc' : 'Province/State/Region', 'op' : lambda : None},
    'country' : {'desc' : 'Country', 'op' : lambda : None},
    'pin' : {'desc' : 'Area PIN code', 'op' : lambda : None},
    'dob' : {'desc' :'Date of Birth', 'op' : lambda : None}
}

# age, sex, income level, race, employment, location, homeownership, and level of education
demographics_config_allowed = {
    'location' : [],
    'age' : [],
    'income-level' : [],
    'race' : [], 
    'employment' : [],
    'homeownership' : [],
    'education-level' : []
}