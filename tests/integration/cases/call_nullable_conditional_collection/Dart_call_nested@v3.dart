dynamic make_widget({dynamic count}) => null;
final my_data = (
make_widget(count: <int>[1, 2]) != null ?
make_widget(count: <int>[1, 2]) // inner
: null // trailing
);
