import java.util.Map;
class Main {
    public static void main() {
var deep = Map.ofEntries(
    Map.entry("_", "_")
);
var my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(Map.entry("b", Map.ofEntries(Map.entry("c", deep)))))
);
    }
}
