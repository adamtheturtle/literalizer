import std.json;
void main() {
int f(T...)(T args) { return 0; }
f(2, "hello");  // trailing note
// next element
f(3, "world");
}
