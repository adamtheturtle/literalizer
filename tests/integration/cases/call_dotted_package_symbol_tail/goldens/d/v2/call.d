import std.json;
void main() {
struct HelperType_ { int list(T...)(T args) { return 0; } }
HelperType_ helper;
helper.list(1);
}
