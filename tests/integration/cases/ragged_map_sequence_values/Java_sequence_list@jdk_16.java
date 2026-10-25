import java.util.Map;
import java.util.List;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", List.of(Map.ofEntries(Map.entry("item", List.of(1))))),
    Map.entry("b", List.of(Map.ofEntries(Map.entry("item", List.of(2, 3)))))
);
    }
}
