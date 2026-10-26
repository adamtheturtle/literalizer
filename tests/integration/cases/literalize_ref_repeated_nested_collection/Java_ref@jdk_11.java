import java.util.Map;
class Main {
    public static void main() {
var shared = new Object[]{
    new int[]{1, 2},
    Map.ofEntries(Map.entry("value", 1))
};
var my_data = new Object[]{
    shared,
    shared
};
    }
}
