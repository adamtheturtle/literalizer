import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(
        Map.entry("b", new int[]{1}),
        // Outdented from the sequence, so the inner mapping claims this.
        Map.entry("c", 2)
    )),
    // Outdented from the inner mapping too, so the root claims this.
    Map.entry("d", 3)
);
my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(
        Map.entry("b", new int[]{1}),
        // Outdented from the sequence, so the inner mapping claims this.
        Map.entry("c", 2)
    )),
    // Outdented from the inner mapping too, so the root claims this.
    Map.entry("d", 3)
);
    }
}
