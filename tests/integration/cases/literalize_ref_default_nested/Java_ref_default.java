import java.util.Map;
class Main {
    public static void main() {
var my_var = Map.ofEntries(
    Map.entry("_", "_")
);
var item_var = Map.ofEntries(
    Map.entry("_", "_")
);
var my_data = Map.ofEntries(
    Map.entry("key", my_var),
    Map.entry("items", new Object[]{item_var, Map.ofEntries(Map.entry("fallback", "value"))})
);
    }
}
