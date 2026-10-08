import std.json;
void main() {
int f(T...)(T args) { return 0; }
auto x = JSONValue(1);
f(x);
}
