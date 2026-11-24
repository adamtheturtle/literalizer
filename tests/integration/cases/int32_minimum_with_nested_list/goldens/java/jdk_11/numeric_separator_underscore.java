import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("minimum", -2_147_483_648),
    Map.entry("neighbor", -2_147_483_647),
    Map.entry("maximum", 2_147_483_647),
    Map.entry("nested", new int[]{-2_147_483_648})
);
    }
}
