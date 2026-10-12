def make_widget(Map _args) { null }
def my_data = (`__LINE__ > 0) ? make_widget(count: 42) : make_widget(count: 42) // trailing `marker
