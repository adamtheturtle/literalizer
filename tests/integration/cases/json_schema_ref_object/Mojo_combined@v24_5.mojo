def main():
    var my_data = {
        "schema": {"$ref": "#/defs/Foo"},
    }
    _ = my_data
    my_data = {
        "schema": {"$ref": "#/defs/Foo"},
    }
    _ = my_data
