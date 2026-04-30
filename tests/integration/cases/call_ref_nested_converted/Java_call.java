import java.util.Map;
class Main {
static Object process(Object... args) { return null; }
    public static void main() {
var myVar = 42;
process(new Object[]{Map.ofEntries(Map.entry("ref", "myVar")), 42, "static"});
    }
}
