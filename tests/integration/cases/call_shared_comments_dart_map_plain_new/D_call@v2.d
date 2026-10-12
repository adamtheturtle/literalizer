import std.json;
void main() {
int make_widget(T...)(T args) { return 0; }
auto my_data = ("${{'value': '// payload'}['value']}").length >= 0 ? make_widget(42) : make_widget(42);
}
