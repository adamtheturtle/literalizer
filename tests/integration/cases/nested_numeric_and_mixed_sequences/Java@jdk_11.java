import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("numbers", new Object[]{1, 2}),
    Map.entry("nested", Map.ofEntries(Map.entry("inner", new int[]{3}))),
    Map.entry("mixed", new Object[]{4, "five"})
);
    }
}
