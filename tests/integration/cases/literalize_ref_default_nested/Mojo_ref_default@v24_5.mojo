def main():
    var item_var = {
        "_": "_",
    }
    var my_data = {
        "items": List([item_var.copy(), {"fallback": "value"}]),
    }
    _ = my_data
