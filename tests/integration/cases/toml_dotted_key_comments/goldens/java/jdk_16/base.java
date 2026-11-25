import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    // first dotted key
    // second dotted key
    Map.entry("a", Map.ofEntries(Map.entry("b", 1), Map.entry("c", 2)))
);
    }
}
