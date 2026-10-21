import std.json;
void main() {
int make_widget(T...)(T args) { return 0; }
make_widget(parseJSON("[]"), JSONValue([JSONValue(1)]), parseJSON("[]"));
make_widget(JSONValue([JSONValue("text")]), JSONValue([JSONValue(2)]), parseJSON("[]"));
make_widget(parseJSON("[]"), JSONValue([JSONValue("text")]), parseJSON("[]"));
make_widget(JSONValue([JSONValue("text")]), JSONValue([JSONValue(2)]), JSONValue([JSONValue(3)]));
}
