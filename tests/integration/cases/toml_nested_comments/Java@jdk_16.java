import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    // About the first dotted key.
    // About the second dotted key.
    Map.entry("dotted", Map.ofEntries(Map.entry("first", 1), Map.entry("second", 2))),
    Map.entry("plain", 3),  // About the plain key.
    // Inside the table.
    Map.entry("table", Map.ofEntries(Map.entry("inner", 4))),
    // Before the first entry.
    // Before the second entry.
    Map.entry("entries", new Object[]{Map.ofEntries(Map.entry("name", "one")), Map.ofEntries(Map.entry("name", "two"))})
);
    }
}
