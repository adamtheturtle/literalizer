import java.util.Map;
class Main {
    public static void main() {
    var shared = new int[]{
        1,
        2
    };
    var my_data = Map.ofEntries(
        Map.entry("a", shared)
    );
    }
}
