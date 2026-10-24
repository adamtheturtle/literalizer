import std.json;
void main() {
struct ObjType_ { int BEGIN(T...)(T args) { return 0; } }
ObjType_ obj;
obj.BEGIN(42);
}
