dynamic make_widget({dynamic before, dynamic populated, dynamic after}) => null;
final my_data = null;
void main() {
    make_widget(before: [], populated: <int>[1], after: []);
    make_widget(before: <String>["text"], populated: <int>[2], after: []);
    make_widget(before: [], populated: <String>["text"], after: []);
    make_widget(before: <String>["text"], populated: <int>[2], after: <int>[3]);
}
