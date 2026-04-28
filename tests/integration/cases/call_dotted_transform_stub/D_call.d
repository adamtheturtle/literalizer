import std.json;
void main() {
int process(T...)(T args) { return 0; }
struct LogType_ { int emit(T...)(T args) { return 0; } }
LogType_ log;
log.emit(process("hello"));
log.emit(process(42));
log.emit(process(true));
}
