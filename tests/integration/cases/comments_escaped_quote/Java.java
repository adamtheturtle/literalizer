import java.util.Map;
class Check {
    Object x = Map.ofEntries(
    Map.entry("key", "value \" # not a comment")  // real
);
}
