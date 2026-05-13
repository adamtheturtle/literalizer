import std.json;
void main() {
int make_widget(T...)(T args) { return 0; }
auto result = JSONValue(make_widget(42));
}
