import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("items", new Object[]{Map.ofEntries(Map.entry("id", 1)), Map.ofEntries(Map.entry("id", 2), Map.entry("count", 10)), Map.ofEntries(Map.entry("id", 3), Map.entry("count", 20))})
);
my_data = Map.ofEntries(
    Map.entry("items", new Object[]{Map.ofEntries(Map.entry("id", 1)), Map.ofEntries(Map.entry("id", 2), Map.entry("count", 10)), Map.ofEntries(Map.entry("id", 3), Map.entry("count", 20))})
);
    }
}
