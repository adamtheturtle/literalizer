import std.json;
void main() {
int make_widget(T...)(T args) { return 0; }
auto my_data = make_widget(42);
make_widget(my_data);
my_data = make_widget(my_data);
make_widget(my_data);
}
