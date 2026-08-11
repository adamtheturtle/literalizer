import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("schema", Map.ofEntries(Map.entry("$ref", "#/defs/Foo")))
);
my_data = Map.ofEntries(
    Map.entry("schema", Map.ofEntries(Map.entry("$ref", "#/defs/Foo")))
);
    }
}
