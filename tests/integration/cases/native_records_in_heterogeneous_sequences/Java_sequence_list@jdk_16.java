import java.util.Map;
import java.util.List;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("h", List.of(1, "a", List.of(2, "b"), Map.ofEntries(Map.entry("k", List.of(true)))))
);
    }
}
