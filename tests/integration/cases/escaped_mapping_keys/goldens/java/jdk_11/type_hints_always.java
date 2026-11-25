import java.util.Map;
class Main {
    public static void main() {
Map<String, Integer> my_data = Map.ofEntries(
    Map.entry("quote\"backslash\\", 1),
    Map.entry("line\nbreak", 2),
    Map.entry("$(literal)${text}", 3),
    Map.entry("RStr prefix", 4)
);
    }
}
