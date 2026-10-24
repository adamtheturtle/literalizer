import java.util.Map;
class Main {
    public static void main() {
Map<String, Object[]> my_data = Map.ofEntries(
    Map.entry("filled", new Object[]{1, "value"}),
    Map.entry("empty", new Object[]{})
);
    }
}
