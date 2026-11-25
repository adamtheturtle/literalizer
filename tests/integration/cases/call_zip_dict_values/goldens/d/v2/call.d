import std.json;
void main() {
int process(T...)(T args) { return 0; }
int emit(T...)(T args) { return 0; }
emit(process("hello"), JSONValue(["a": JSONValue(1), "b": JSONValue(2)]));
emit(process(42), JSONValue(["c": JSONValue(3), "d": JSONValue(4)]));
}
