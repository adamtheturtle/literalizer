import java.util.Map;
import java.util.List;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("lint", List.of(2, List.of())),
    Map.entry("test", List.of(5, List.of("compile"))),
    Map.entry("package", List.of(7, List.of("link", "test")))
);
    }
}
