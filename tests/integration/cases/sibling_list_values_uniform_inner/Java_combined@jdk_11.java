import java.util.Map;
class Main {
    public static void main() {
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
