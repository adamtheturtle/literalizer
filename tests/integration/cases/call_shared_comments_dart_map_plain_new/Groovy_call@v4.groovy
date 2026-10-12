def make_widget(Map _args) { null }
def my_data = ("${{'value': '// payload'}['value']}").length >= 0 ? make_widget(count: 42) : make_widget(count: 42)
