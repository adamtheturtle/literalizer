import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("positive", new Object[]{Map.ofEntries(Map.entry("item", new long[]{2147483648L}))}),
    Map.entry("negative", new Object[]{Map.ofEntries(Map.entry("item", new long[]{-2147483649L}))}),
    Map.entry("mixed", new Object[]{Map.ofEntries(Map.entry("item", new long[]{0, 2147483648L}))})
);
    }
}
