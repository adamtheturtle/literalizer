dynamic make_widget({dynamic count}) => null;
final my_data = make_widget(count: 42) ?
make_widget(count: 42) // inner
: nil; // trailing
