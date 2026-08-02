import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("""
outer""", new String[][]{new String[]{"""
nested first line
  indented

nested last line
"""}})
);
    }
}
