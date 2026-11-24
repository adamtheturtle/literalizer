import java.util.Map;
class Main {
static Object process(Object arg0) { return null; }
static Object emit(Object arg0, Object arg1) { return null; }
    public static void main() {
emit(process("hello"), Map.ofEntries(Map.entry("a", 1), Map.entry("b", 2)));
emit(process(42), Map.ofEntries(Map.entry("c", 3), Map.entry("d", 4)));
    }
}
