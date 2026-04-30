import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto my_var = JSONValue(42);
process(JSONValue([my_var, JSONValue(42), JSONValue("static")]));
}
