import std.json;
void main() {
struct ObjType_ { int ZVal(T...)(T args) { return 0; } }
ObjType_ obj;
obj.ZVal(1);
}
