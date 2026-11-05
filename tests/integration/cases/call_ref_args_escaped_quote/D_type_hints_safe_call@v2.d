import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto my_str = JSONValue("a\"b");
process(my_str);
}
