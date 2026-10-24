import java.util.Map;
class Main {
    public static void main() {
var shared = new Object[]{
    Map.ofEntries(Map.entry("value", 1))
};
var my_data = new Object[]{
    shared,
    shared
};
    }
}
