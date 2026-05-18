import java.util.Map;
class Main {
static Object process(Object... args) { return null; }
static Object emit(Object... args) { return null; }
    public static void main() {
emit(process("hello"), Map.ofEntries(Map.entry("a", 1), Map.entry("b", 2)));
emit(process(42), Map.ofEntries(Map.entry("c", 3), Map.entry("d", 4)));
    }
}
