import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto my_var = JSONValue(42);
auto my_other = JSONValue(7);
process(JSONValue([my_var, JSONValue(42), JSONValue("static")]));
process(JSONValue([my_other, JSONValue(7), JSONValue("label")]));
}
