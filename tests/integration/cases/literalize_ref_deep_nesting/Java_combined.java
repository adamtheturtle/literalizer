import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(Map.entry("b", Map.ofEntries(Map.entry("c", Map.ofEntries(Map.entry("$ref", "deep")))))))
);
my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(Map.entry("b", Map.ofEntries(Map.entry("c", Map.ofEntries(Map.entry("$ref", "deep")))))))
);
    }
}
