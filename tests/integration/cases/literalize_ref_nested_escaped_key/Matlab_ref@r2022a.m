foo = struct(
    '_', "_"
);
my_data = struct(
    'items', {{struct('other', 1), foo}},
    'mapping', struct('value', foo)
);
