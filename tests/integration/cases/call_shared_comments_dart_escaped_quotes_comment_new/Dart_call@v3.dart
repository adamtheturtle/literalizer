dynamic make_widget({dynamic count}) => null;
final my_data = ("\"prefix ${"// payload"}\"").length >= 0 ? make_widget(count: 42) : make_widget(count: 42); // trailing
// extra
