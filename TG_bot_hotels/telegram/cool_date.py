lst = [
    {'checkInDate': {'year': 2024, 'month': 5, 'day': 14}},
    {'checkOutDate': {'year': 2024, 'month': 9, 'day': 20}},
    {'rooms': [{'adults': '2', 'children': '2'}, {'adults': '2', 'children': '1'}, {}]},
    {'city': 'Ottawa'}
]

for item in lst:
    if 'city' in item:
        city_value = item['city']
        if city_value.isdigit():
            print(f"{city_value} - это число")
        else:
            print(f"{city_value} - это не число")



