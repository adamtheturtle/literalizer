import std.json;
void main() {
int f(T...)(T args) { return 0; }
auto ref_data = JSONValue(1);
f(ref_data);
}
