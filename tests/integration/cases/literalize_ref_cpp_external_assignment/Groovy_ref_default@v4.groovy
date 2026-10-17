def consume_widget(Map _args) { null }
def ref_data = [
    1,
    2,
]
def my_data = [
    0,
]
consume_widget(_arg: my_data)
my_data = ref_data
consume_widget(_arg: my_data)
