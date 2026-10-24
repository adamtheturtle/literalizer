import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", 1),
    Map.entry("b", 3_000_000_000L),
    Map.entry("c", "x")
);
    }
}
