import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(Map.entry("k", "2040-01-01T00:00:00+00:00"))),
    Map.entry("b", Map.ofEntries(Map.entry("k", 1)))
);
    }
}
