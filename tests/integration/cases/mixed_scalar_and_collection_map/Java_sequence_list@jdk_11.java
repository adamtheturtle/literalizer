import java.util.Map;
import java.util.List;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", 1),
    Map.entry("b", "x"),
    Map.entry("e", List.of(1, 2)),
    Map.entry("f", Map.ofEntries(Map.entry("g", "h")))
);
    }
}
