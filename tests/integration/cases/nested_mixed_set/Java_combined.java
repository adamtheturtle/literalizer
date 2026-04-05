import java.util.Map;
import java.util.Set;
class Check {
    public static void check() {
var my_data = Map.ofEntries(
    Map.entry("name", "Alice"),
    Map.entry("tags", Set.of(true, 42, "apple"))
);
my_data = Map.ofEntries(
    Map.entry("name", "Alice"),
    Map.entry("tags", Set.of(true, 42, "apple"))
);
    }
}
