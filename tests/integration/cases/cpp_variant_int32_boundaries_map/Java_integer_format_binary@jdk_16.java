import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("below", -0b10000000000000000000000000000001L),
    Map.entry("minimum", -0b10000000000000000000000000000000),
    Map.entry("above", -0b1111111111111111111111111111111),
    Map.entry("nested", new int[]{0b0})
);
    }
}
