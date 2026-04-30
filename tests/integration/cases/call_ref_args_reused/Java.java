import java.util.Map;
class Main {
    public static void main() {
var my_data = new Object[]{
    new Object[]{Map.ofEntries(Map.entry("$ref", "repeated_var")), 1},
    new Object[]{Map.ofEntries(Map.entry("$ref", "single_var")), 0},
    new Object[]{Map.ofEntries(Map.entry("$ref", "repeated_var")), 8}
};
    }
}
