import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("deep", new int[][][][]{new int[][][]{new int[][]{new int[]{1}}}})
);
my_data = Map.ofEntries(
    Map.entry("deep", new int[][][][]{new int[][][]{new int[][]{new int[]{1}}}})
);
    }
}
