import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(Map.entry("x", 1))),
    Map.entry("b", 2)
);
    }
}
