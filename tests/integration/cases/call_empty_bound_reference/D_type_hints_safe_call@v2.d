import std.json;
void main() {
int make_widget(T...)(T args) { return 0; }
auto items = parseJSON("[]");
make_widget(items);
}
