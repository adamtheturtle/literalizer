import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    // heading
    Map.entry("a", "single ' // data"),
    Map.entry("b", "linecontinuation"),
    Map.entry("c", "\\"),  // actual comment
    Map.entry("d", "  ")  // final comment
);
    }
}
