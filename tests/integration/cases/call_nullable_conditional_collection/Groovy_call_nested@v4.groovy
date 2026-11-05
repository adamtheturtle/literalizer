def make_widget(Map _args) { null }
def my_data = (
make_widget(count: [1, 2]) != null ?
make_widget(count: [1, 2]) // inner
: null // trailing
)
