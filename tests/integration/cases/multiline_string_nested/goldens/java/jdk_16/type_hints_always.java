import java.util.Map;
class Main {
    public static void main() {
Map<String, String[][]> my_data = Map.ofEntries(
    Map.entry("outer", new String[][]{new String[]{"nested first line\n  indented\n\nnested last line\n"}})
);
    }
}
