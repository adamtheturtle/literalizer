import java.util.Map;
class Main {
    public static void main() {
var my_data = new Object[]{
    Map.ofEntries(Map.entry("input", Map.ofEntries(Map.entry("name", "alice"), Map.entry("city", "paris"))), Map.entry("expected", Map.ofEntries(Map.entry("count", 1), Map.entry("total", 2)))),
    Map.ofEntries(Map.entry("input", Map.ofEntries(Map.entry("name", 10), Map.entry("city", 20))), Map.entry("expected", Map.ofEntries(Map.entry("count", "done"), Map.entry("total", "pending"))))
};
    }
}
