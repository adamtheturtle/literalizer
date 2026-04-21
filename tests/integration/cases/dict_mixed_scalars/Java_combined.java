import java.util.Map;
class Check {
    public static void check() {
var my_data = Map.ofEntries(
    Map.entry("a", 1),
    Map.entry("b", "x")
);
my_data = Map.ofEntries(
    Map.entry("a", 1),
    Map.entry("b", "x")
);
    }
}
