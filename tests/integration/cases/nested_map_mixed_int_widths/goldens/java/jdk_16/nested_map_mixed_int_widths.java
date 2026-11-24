import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("p", Map.ofEntries(Map.entry("a", 1L))),
    Map.entry("q", Map.ofEntries(Map.entry("a", 1099511627776L)))
);
    }
}
