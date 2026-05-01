my_var = struct(
    '_', "_"
);
item_var = struct(
    '_', "_"
);
my_data = struct(
    'key', my_var,
    'items', {{item_var, struct('fallback', "value")}}
);
