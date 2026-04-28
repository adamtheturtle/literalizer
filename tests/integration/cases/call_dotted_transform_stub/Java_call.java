class Main {
static Object process(Object... args) { return null; }
static class LogType_ { Object emit(Object... args) { return null; } }
static LogType_ log = new LogType_();
    public static void main() {
log.emit(process("hello"));
log.emit(process(42));
log.emit(process(true));
    }
}
