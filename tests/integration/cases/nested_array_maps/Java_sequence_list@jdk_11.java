import java.util.Map;
import java.util.List;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("groups", List.of(List.of(Map.ofEntries(Map.entry("id", 1))), List.of(Map.ofEntries(Map.entry("id", 2)))))
);
    }
}
