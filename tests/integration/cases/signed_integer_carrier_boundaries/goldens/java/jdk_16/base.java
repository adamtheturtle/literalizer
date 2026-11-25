import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("i32_below", -2147483649L),
    Map.entry("i32_minimum", -2147483648L),
    Map.entry("i32_above", -2147483647L),
    Map.entry("i32_maximum", 2147483647L),
    Map.entry("i32_over", 2147483648L),
    Map.entry("i64_minimum", -9223372036854775808L),
    Map.entry("i64_maximum", 9223372036854775807L)
);
    }
}
