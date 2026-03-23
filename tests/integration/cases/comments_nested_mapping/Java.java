import java.util.Map;
class Check {
    Object x = Map.ofEntries(
    Map.entry("a", Map.ofEntries(Map.entry("x", 1))),
    Map.entry("b", 2)
);
}
