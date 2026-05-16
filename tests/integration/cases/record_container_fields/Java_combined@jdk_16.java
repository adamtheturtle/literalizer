import java.util.Map;
import java.util.Set;
class Main {
    public static void main() {
var my_data = new Object[]{
    Map.ofEntries(Map.entry("id", 1), Map.entry("empty_map", Map.ofEntries()), Map.entry("int_map", Map.ofEntries(Map.entry(1, "a"))), Map.entry("full_set", Set.of("x", "y")), Map.entry("empty_set", Set.of())),
    Map.ofEntries(Map.entry("id", 2), Map.entry("empty_map", Map.ofEntries()), Map.entry("int_map", Map.ofEntries(Map.entry(1, "b"))), Map.entry("full_set", Set.of("x")), Map.entry("empty_set", Set.of()))
};
my_data = new Object[]{
    Map.ofEntries(Map.entry("id", 1), Map.entry("empty_map", Map.ofEntries()), Map.entry("int_map", Map.ofEntries(Map.entry(1, "a"))), Map.entry("full_set", Set.of("x", "y")), Map.entry("empty_set", Set.of())),
    Map.ofEntries(Map.entry("id", 2), Map.entry("empty_map", Map.ofEntries()), Map.entry("int_map", Map.ofEntries(Map.entry(1, "b"))), Map.entry("full_set", Set.of("x")), Map.entry("empty_set", Set.of()))
};
    }
}
