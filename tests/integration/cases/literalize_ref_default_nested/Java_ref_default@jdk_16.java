import java.util.Map;
class Main {
    public static void main() {
var item_var = Map.ofEntries(
    Map.entry("_", "_")
);
var my_data = Map.ofEntries(
    Map.entry("items", new Object[]{item_var, Map.ofEntries(Map.entry("fallback", "value"))})
);
    }
}
