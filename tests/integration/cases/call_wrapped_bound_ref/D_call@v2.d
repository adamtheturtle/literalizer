import std.json;
void main() {
int make_widget(T...)(T args) { return 0; }
auto value = JSONValue(1);
make_widget(value);
}
