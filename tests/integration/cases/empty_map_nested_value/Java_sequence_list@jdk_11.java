import java.util.Map;
import java.util.List;
class Main {
    public static void main() {
var my_data = List.of(
    List.of(Map.ofEntries(Map.entry("mapping", Map.ofEntries())), Map.ofEntries()),
    List.of(Map.ofEntries(), Map.ofEntries(Map.entry("mapping", Map.ofEntries())))
);
    }
}
