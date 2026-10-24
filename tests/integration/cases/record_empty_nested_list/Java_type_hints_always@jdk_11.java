import java.util.Map;
class Main {
    public static void main() {
Map<String, Object> my_data = Map.ofEntries(
    Map.entry("a", new int[][]{new int[]{1, 2}, new int[]{3}}),
    Map.entry("b", new int[][]{new int[]{}, new int[]{1}})
);
    }
}
