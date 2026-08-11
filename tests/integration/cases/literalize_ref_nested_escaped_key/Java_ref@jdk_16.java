import java.util.Map;
class Main {
    public static void main() {
var foo = Map.ofEntries(
    Map.entry("_", "_")
);
var my_data = Map.ofEntries(
    Map.entry("items", new Object[]{Map.ofEntries(Map.entry("other", 1)), foo}),
    Map.entry("mapping", Map.ofEntries(Map.entry("value", foo)))
);
    }
}
