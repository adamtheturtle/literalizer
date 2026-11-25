import std.json;
void main() {
int f(T...)(T args) { return 0; }
int repr(T...)(T args) { return 0; }
auto ref_data = JSONValue(1);
repr(f(ref_data));
}
