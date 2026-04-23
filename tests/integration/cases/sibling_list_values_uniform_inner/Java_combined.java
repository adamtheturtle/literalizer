import java.util.Map;
class Check {
    public static void check() {
var my_data = Map.ofEntries(
    Map.entry("lint", new Object[]{2, new int[]{1}}),
    Map.entry("test", new Object[]{5, new int[]{7}})
);
my_data = Map.ofEntries(
    Map.entry("lint", new Object[]{2, new int[]{1}}),
    Map.entry("test", new Object[]{5, new int[]{7}})
);
    }
}
