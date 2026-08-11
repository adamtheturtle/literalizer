foo = struct(
    '_', "_"
);
my_data = struct(
    'mapping', struct('value', foo),
    'items', {{struct('other', 1), foo}}
);
