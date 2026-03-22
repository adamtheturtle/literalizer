import java.util.Map;
class Check {
    public static void check() {
var my_data = Map.ofEntries(
    Map.entry("key\nwith\nnewlines", "value1"),
    Map.entry("key\twith\ttabs", "value2"),
    Map.entry("", "value3")
);
my_data = Map.ofEntries(
    Map.entry("key\nwith\nnewlines", "value1"),
    Map.entry("key\twith\ttabs", "value2"),
    Map.entry("", "value3")
);
    }
}
