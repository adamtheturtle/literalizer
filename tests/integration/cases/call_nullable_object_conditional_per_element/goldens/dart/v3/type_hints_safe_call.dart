dynamic make_widget({dynamic count}) => null;
final my_data = make_widget(count: 7) != null ?
make_widget(count: 7) // inner
: null; // trailing
