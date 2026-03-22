import java.util.Map;
import java.util.Set;
class Check {
    public static void check() {
var my_data = Map.ofEntries(
    Map.entry("key\nwith\nnewlines", "value1"),
    Map.entry("key\twith\ttabs", "value2"),
    Map.entry("", "value3")
);
    }
}
