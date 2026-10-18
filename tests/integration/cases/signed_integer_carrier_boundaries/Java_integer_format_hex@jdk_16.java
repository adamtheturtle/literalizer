import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("i32_below", -0x80000001L),
    Map.entry("i32_minimum", -0x80000000L),
    Map.entry("i32_above", -0x7fffffffL),
    Map.entry("i32_maximum", 0x7fffffffL),
    Map.entry("i32_over", 0x80000000L),
    Map.entry("i64_minimum", -0x8000000000000000L),
    Map.entry("i64_maximum", 0x7fffffffffffffffL)
);
    }
}
