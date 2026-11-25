import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("i32_below", -020000000001L),
    Map.entry("i32_minimum", -020000000000L),
    Map.entry("i32_above", -017777777777L),
    Map.entry("i32_maximum", 017777777777L),
    Map.entry("i32_over", 020000000000L),
    Map.entry("i64_minimum", -01000000000000000000000L),
    Map.entry("i64_maximum", 0777777777777777777777L)
);
    }
}
