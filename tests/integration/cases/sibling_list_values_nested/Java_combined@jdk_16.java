import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("lint", new Object[]{2, new Object[]{}}),
    Map.entry("test", new Object[]{5, new Object[]{"compile"}})
);
my_data = Map.ofEntries(
    Map.entry("lint", new Object[]{2, new Object[]{}}),
    Map.entry("test", new Object[]{5, new Object[]{"compile"}})
);
    }
}
