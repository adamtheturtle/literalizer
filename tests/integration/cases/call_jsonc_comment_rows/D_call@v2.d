import std.json;
void main() {
int f(T...)(T args) { return 0; }
// calls heading
// before call one
// first argument
f(1, 2);  // after call one
// second argument
f(3, 4);
// after all calls
}
