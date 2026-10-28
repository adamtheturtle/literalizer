import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("below", -0x80000001L),
    Map.entry("minimum", -0x80000000),
    Map.entry("above", -0x7fffffff),
    Map.entry("nested", new int[]{0x0})
);
    }
}
