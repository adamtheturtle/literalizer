import java.util.Map;
import java.util.List;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("_", List.of(Map.ofEntries(Map.entry("type", "create"), Map.entry("name", "a")), Map.ofEntries(Map.entry("type", "update"), Map.entry("name", "b"))))
);
    }
}
