import std.json;
void main() {
struct ThingType_ { int go(T...)(T args) { return 0; } }
ThingType_ thing;
thing.go(parseJSON("[]"), JSONValue([JSONValue(1)]), parseJSON("[]"));
thing.go(JSONValue([JSONValue("text")]), JSONValue([JSONValue(2)]), parseJSON("[]"));
thing.go(parseJSON("[]"), JSONValue([JSONValue("text")]), parseJSON("[]"));
thing.go(JSONValue([JSONValue("text")]), JSONValue([JSONValue(2)]), JSONValue([JSONValue(3)]));
}
