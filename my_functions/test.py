import pandas as pd
graph = {'a': {'w': 14, 'x': 7, 'y': 9},
            'b': {'w': 9, 'z': 6},
            'w': {'a': 14, 'b': 9, 'y': 2},
            'x': {'a': 7, 'y': 10, 'z': 15},
            'y': {'a': 9, 'w': 2, 'x': 10, 'z': 11},
            'z': {'b': 6, 'x': 15, 'y': 11}}

df = pd.DataFrame(data=graph)

print df.head()