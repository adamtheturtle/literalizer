import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    // outer heading
    // first empty
    Map.entry("a", Map.ofEntries()),
    // second empty
    Map.entry("b", Map.ofEntries())
);
    }
}
