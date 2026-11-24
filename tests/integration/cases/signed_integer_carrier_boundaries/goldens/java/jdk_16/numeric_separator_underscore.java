import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("i32_below", -2_147_483_649L),
    Map.entry("i32_minimum", -2_147_483_648L),
    Map.entry("i32_above", -2_147_483_647L),
    Map.entry("i32_maximum", 2_147_483_647L),
    Map.entry("i32_over", 2_147_483_648L),
    Map.entry("i64_minimum", -9_223_372_036_854_775_808L),
    Map.entry("i64_maximum", 9_223_372_036_854_775_807L)
);
    }
}
