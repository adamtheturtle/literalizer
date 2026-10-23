import java.util.Map;
class Main {
    public static void main() {
Map<String, Object> my_data = Map.ofEntries(
    Map.entry("name", "Ada"),
    Map.entry("active", true),
    Map.entry("scores", new int[]{1, 2, 3})
);
    }
}
