import java.util.Map;
class Check {
    public static void check() {
var my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(Map.entry("x", 1))),
    Map.entry("b", 2)
);
my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(Map.entry("x", 1))),
    Map.entry("b", 2)
);
    }
}
