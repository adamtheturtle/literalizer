import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("ordered", new java.util.ArrayList<>(java.util.Arrays.asList(
        // ordered entry
        Map.entry("name", "Alice"),
        Map.entry("scores", Map.ofEntries(
            // score meaning
            Map.entry(1, "first"),
            Map.entry(2, "second")  // latest score
        ))
    )))
);
my_data = Map.ofEntries(
    Map.entry("ordered", new java.util.ArrayList<>(java.util.Arrays.asList(
        // ordered entry
        Map.entry("name", "Alice"),
        Map.entry("scores", Map.ofEntries(
            // score meaning
            Map.entry(1, "first"),
            Map.entry(2, "second")  // latest score
        ))
    )))
);
    }
}
