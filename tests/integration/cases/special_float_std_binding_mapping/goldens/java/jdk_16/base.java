import java.util.Map;
class Main {
    public static void main() {
var std = Map.ofEntries(
    Map.entry("nan", Double.NaN),
    Map.entry("positive", Double.POSITIVE_INFINITY),
    Map.entry("negative", Double.NEGATIVE_INFINITY)
);
    }
}
