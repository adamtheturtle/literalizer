import java.util.Map;
import java.util.Set;
class Check {
    Object x = Map.ofEntries(
    Map.entry("key\nwith\nnewlines", "value1"),
    Map.entry("key	with	tabs", "value2")
);
}
