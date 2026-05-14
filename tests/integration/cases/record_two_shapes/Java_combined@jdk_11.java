import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("metrics", Map.ofEntries(Map.entry("count", 100), Map.entry("rate", 50))),
    Map.entry("flags", Map.ofEntries(Map.entry("retries", 3), Map.entry("timeout", 30)))
);
my_data = Map.ofEntries(
    Map.entry("metrics", Map.ofEntries(Map.entry("count", 100), Map.entry("rate", 50))),
    Map.entry("flags", Map.ofEntries(Map.entry("retries", 3), Map.entry("timeout", 30)))
);
    }
}
