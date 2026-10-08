import java.util.Map;
class Main {
    public static void main() {
var siblingMap = Map.ofEntries(
    Map.entry("k", 2)
);
var my_data = new Object[]{
    Map.ofEntries(Map.entry("k", 1)),
    siblingMap
};
    }
}
