import java.util.Map;
class Main {
static Object process(Object... args) { return null; }
    public static void main() {
var my_var = 42;
var my_other = 7;
process(new Object[]{Map.ofEntries(Map.entry("ref", "my_var")), 42, "static"});
process(new Object[]{Map.ofEntries(Map.entry("ref", "my_other")), 7, "label"});
    }
}
