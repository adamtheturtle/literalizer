import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("outer", new Object[]{Map.ofEntries(Map.entry("_", 1))})
);
    }
}
