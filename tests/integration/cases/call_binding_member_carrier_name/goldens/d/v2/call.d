import std.json;
void main() {
struct ObjType_ { int ZVal(T...)(T args) { return 0; } }
ObjType_ obj;
auto my_data = obj.ZVal(42); // note
}
