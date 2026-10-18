import java.util.HashMap;
import java.util.Map;
class Main {
    public static void main() {
var my_data = new HashMap<>(Map.ofEntries(
    Map.entry("positive", Double.POSITIVE_INFINITY),
    Map.entry("negative", Double.NEGATIVE_INFINITY),
    Map.entry("nan_value", Double.NaN),
    Map.entry("finite", 1.5)
));
    }
}
