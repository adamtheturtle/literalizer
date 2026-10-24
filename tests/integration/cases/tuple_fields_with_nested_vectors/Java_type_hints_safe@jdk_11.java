import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("lint", new Object[]{2, new Object[]{}}),
    Map.entry("test", new Object[]{5, new String[]{"compile"}}),
    Map.entry("package", new Object[]{7, new String[]{"link", "test"}})
);
    }
}
