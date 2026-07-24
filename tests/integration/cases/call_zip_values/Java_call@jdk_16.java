class Main {
static Object process(Object... args) { return null; }
static Object emit(Object... args) { return null; }
    public static void main() {
emit(process("hello"), 1);
emit(process(42), 0);
    }
}
