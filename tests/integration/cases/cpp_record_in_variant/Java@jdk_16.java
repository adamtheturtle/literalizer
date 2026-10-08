import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("h", new Object[]{1, "a", new Object[]{2, "b"}, Map.ofEntries(Map.entry("k", new boolean[]{true}))})
);
    }
}
