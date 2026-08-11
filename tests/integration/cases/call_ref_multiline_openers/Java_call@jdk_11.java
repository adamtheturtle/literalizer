import java.util.Map;
class Main {
static Object consume(Object... args) { return null; }
    public static void main() {
var foo = 42;
consume(new Object[]{
    Map.ofEntries(
        Map.entry("other", 1)
    ),
    foo
}, Map.ofEntries(
    Map.entry("left", foo),
    Map.entry("other", 1)
));
    }
}
