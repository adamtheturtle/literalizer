import java.util.Map;
class Main {
    public static void main() {
var my_data = new java.util.ArrayList<>(java.util.Arrays.asList(
    Map.entry("name", "Alice"),
    Map.entry("scores", Map.ofEntries(
        // score meaning
        Map.entry(1, "first"),
        Map.entry(2, "second")  // latest score
    ))
));
    }
}
