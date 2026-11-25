import std.json;
void main() {
int process(T...)(T args) { return 0; }
int emit(T...)(T args) { return 0; }
emit(process(42), true);
}
