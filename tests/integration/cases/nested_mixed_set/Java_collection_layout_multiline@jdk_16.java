import java.util.Map;
import java.util.Set;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("name", "Alice"),
    Map.entry("tags", Set.of(
        true,
        42,
        "apple"
    ))
);
    }
}
