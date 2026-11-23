import java.util.Map;
class Main {
    public static void main() {
var sharedValues = new int[]{
    1,
    2
};
var my_data = Map.ofEntries(
    Map.entry("a", sharedValues)
);
my_data = Map.ofEntries(
    Map.entry("a", sharedValues)
);
    }
}
