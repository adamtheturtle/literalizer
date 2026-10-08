import java.util.Map;
import java.util.List;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("d", List.of(Map.ofEntries(Map.entry("a", List.of(Map.ofEntries(Map.entry("b", List.of(1, List.of(2.5, List.of("x", List.of(true)))))))))))
);
    }
}
