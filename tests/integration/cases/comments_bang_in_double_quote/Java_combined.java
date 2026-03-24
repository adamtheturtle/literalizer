import java.util.Map;
class Check {
    public static void check() {
var my_data = Map.ofEntries(
    Map.entry("key", "\"bang!\"")  // real
);
my_data = Map.ofEntries(
    Map.entry("key", "\"bang!\"")  // real
);
    }
}
