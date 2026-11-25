import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("minimum", -2147483648),
    Map.entry("neighbor", -2147483647),
    Map.entry("maximum", 2147483647),
    Map.entry("nested", new int[]{-2147483648})
);
    }
}
