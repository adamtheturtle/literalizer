import java.util.Map;
class Main {
    public static void main() {
var sharedVar = Map.ofEntries(
    Map.entry("_", "_")
);
var my_data = new Object[]{
    sharedVar,
    sharedVar
};
    }
}
