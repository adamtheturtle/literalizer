import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("key\nwith\nnewlines", "value1"),
    Map.entry("key\twith\ttabs", "value2"),
    Map.entry("", "value3")
);
    }
}
