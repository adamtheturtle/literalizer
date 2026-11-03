import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("lists", new Object[]{new int[]{1}, new String[]{"x"}, new Object[]{}}),
    Map.entry("maps", new Object[]{Map.ofEntries(Map.entry("x", 1)), Map.ofEntries(Map.entry("x", "s"))}),
    Map.entry("empties", Map.ofEntries(Map.entry("a", new int[]{1}), Map.entry("b", new int[]{})))
);
    }
}
