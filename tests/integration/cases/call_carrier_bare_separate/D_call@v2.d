import std.json;
void main() {
int make_widget(T...)(T args) { return 0; }
make_widget(JSONValue([JSONValue(1)]), JSONValue([JSONValue("text")]));
}
