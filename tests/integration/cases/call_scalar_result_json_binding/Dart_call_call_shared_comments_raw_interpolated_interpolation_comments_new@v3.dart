dynamic make_widget({dynamic count}) => null;
final my_data = ("${ /* } " block */ 42 // } " line
}").length >= 0 ? make_widget(count: 42) : make_widget(count: 42); // trailing
// extra
