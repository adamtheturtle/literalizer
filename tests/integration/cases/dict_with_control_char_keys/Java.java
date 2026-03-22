import java.util.Map;
class Check {
    Object x = Map.ofEntries(
    Map.entry("key\nwith\nnewlines", "value1"),
    Map.entry("key\twith\ttabs", "value2"),
    Map.entry("", "value3")
);
}
