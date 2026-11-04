dynamic make_widget({dynamic before, dynamic populated, dynamic after}) => null;
final my_data = null;
void main() {
    make_widget(before: (), populated: (1,), after: ());
    make_widget(before: ("text",), populated: (2,), after: ());
    make_widget(before: (), populated: ("text",), after: ());
    make_widget(before: ("text",), populated: (2,), after: (3,));
}
