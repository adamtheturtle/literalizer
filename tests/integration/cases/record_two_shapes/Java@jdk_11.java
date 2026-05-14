import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("user", Map.ofEntries(Map.entry("id", 1), Map.entry("name", "Alice"))),
    Map.entry("project", Map.ofEntries(Map.entry("title", "report"), Map.entry("tags", new String[]{"draft", "urgent"})))
);
    }
}
