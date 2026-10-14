import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("below", -2147483649L),
    Map.entry("minimum", -2147483648L),
    Map.entry("above", -2147483647L),
    Map.entry("nested", new long[]{0L})
);
    }
}
