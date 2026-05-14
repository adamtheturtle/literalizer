import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto my_var = JSONValue(42);
process(JSONValue(["key": my_var, "count": JSONValue(42)]));
}
