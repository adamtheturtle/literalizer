import java.util.Map;
class Check {
    Object my_data = Map.ofEntries(
    Map.entry("key", "value \" # not a comment")  // real
);
}
