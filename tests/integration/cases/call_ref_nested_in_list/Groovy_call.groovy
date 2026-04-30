def process(Map _args) { null }
def my_var = 42
def my_other = 7
process(data: [["ref": "my_var"], 42, "static"])
process(data: [["ref": "my_other"], 7, "label"])
