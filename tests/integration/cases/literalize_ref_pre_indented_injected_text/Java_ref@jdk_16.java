import java.util.Map;
class Main {
    public static void main() {
            var shared = new int[]{
                1,
                2
            };
            var other = 3;
            var payload = "\n    shared : Val\nshared = RInt 99";
            var my_data = Map.ofEntries(
                Map.entry("a", shared),
                Map.entry("b", other),
                Map.entry("payload", payload)
            );
    }
}
