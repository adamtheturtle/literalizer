import java.util.Map;
class Check {
    public static void check() {
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
