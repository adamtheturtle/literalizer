import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("rows", new Object[]{Map.ofEntries(Map.entry("x", 1), Map.entry("y", "a")), Map.ofEntries(Map.entry("x", 2), Map.entry("y", "b"))})
);
    }
}
