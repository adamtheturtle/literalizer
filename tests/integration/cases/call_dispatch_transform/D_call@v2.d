import std.json;
void main() {
int record_value(T...)(T args) { return 0; }
int flush_buffer(T...)(T args) { return 0; }
int emit(T...)(T args) { return 0; }
emit(record_value(42));
flush_buffer(3);
}
