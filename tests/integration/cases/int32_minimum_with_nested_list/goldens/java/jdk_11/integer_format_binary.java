import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("minimum", -0b10000000000000000000000000000000),
    Map.entry("neighbor", -0b1111111111111111111111111111111),
    Map.entry("maximum", 0b1111111111111111111111111111111),
    Map.entry("nested", new int[]{-0b10000000000000000000000000000000})
);
    }
}
