import std.json;
void main() {
int process(T...)(T args) { return 0; }
struct HelpersType_ { int emit(T...)(T args) { return 0; } }
HelpersType_ helpers;
helpers.emit(process(1), 42);
}
