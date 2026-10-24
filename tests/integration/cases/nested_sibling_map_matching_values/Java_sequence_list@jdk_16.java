import java.util.Map;
import java.util.List;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("first", Map.ofEntries(Map.entry("items", List.of(1, Map.ofEntries(Map.entry("value", 2)))))),
    Map.entry("second", Map.ofEntries(Map.entry("items", List.of(1, Map.ofEntries(Map.entry("value", 3))))))
);
    }
}
