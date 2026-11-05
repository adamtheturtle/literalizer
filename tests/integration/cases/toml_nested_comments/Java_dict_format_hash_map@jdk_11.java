import java.util.HashMap;
import java.util.Map;
class Main {
    public static void main() {
var my_data = new HashMap<>(Map.ofEntries(
    // About the first dotted key.
    // About the second dotted key.
    Map.entry("dotted", new HashMap<>(Map.ofEntries(Map.entry("first", 1), Map.entry("second", 2)))),
    Map.entry("plain", 3),  // About the plain key.
    // Before the first entry.
    // Before the second entry.
    Map.entry("entries", new Object[]{new HashMap<>(Map.ofEntries(Map.entry("name", "one"))), new HashMap<>(Map.ofEntries(Map.entry("name", "two")))}),
    // Inside the table.
    Map.entry("table", new HashMap<>(Map.ofEntries(Map.entry("inner", 4))))
));
    }
}
