import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("single_map", new Object[]{Map.ofEntries()}),
    Map.entry("single_list", new Object[]{new Object[]{1}}),
    Map.entry("single_deep", new Object[]{new Object[]{new int[]{2}}})
);
    }
}
