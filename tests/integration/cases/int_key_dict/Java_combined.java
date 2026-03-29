import java.util.Map;
class Check {
    public static void check() {
var my_data = Map.ofEntries(
    Map.entry("1", "one"),
    Map.entry("2", "two"),
    Map.entry("42", "answer")
);
my_data = Map.ofEntries(
    Map.entry("1", "one"),
    Map.entry("2", "two"),
    Map.entry("42", "answer")
);
    }
}
