import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("astral", "😀"),
    Map.entry("mixed", "a😀b"),
    Map.entry("count", 2),
    Map.entry("list", new Object[]{"😀", 1}),
    Map.entry("nested", Map.ofEntries(Map.entry("inner", "😀")))
);
    }
}
