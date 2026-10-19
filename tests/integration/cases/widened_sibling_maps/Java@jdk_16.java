import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(Map.entry("k", 1))),
    Map.entry("b", Map.ofEntries(Map.entry("k", "s")))
);
    }
}
