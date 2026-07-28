import java.util.Map;
class Main {
static Object process(Object... args) { return null; }
    public static void main() {
var my_list = Map.ofEntries(
    Map.entry("unused", "value")
);
process(new Object[]{new Object[]{Map.ofEntries(Map.entry("inner", my_list))}});
    }
}
