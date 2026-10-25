import std.json;
void main() {
int process(T...)(T args) { return 0; }
process(JSONValue(["value": JSONValue(1)]));
process(JSONValue(["value": JSONValue("hello")]));
}
