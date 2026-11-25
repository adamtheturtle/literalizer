import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("true_to_one", Map.ofEntries(Map.entry("value", 1))),
    Map.entry("one_to_true", Map.ofEntries(Map.entry("value", true))),
    Map.entry("false_to_zero", Map.ofEntries(Map.entry("value", 0))),
    Map.entry("zero_to_false", Map.ofEntries(Map.entry("value", false))),
    Map.entry("nested_boolean_to_float", Map.ofEntries(Map.entry("value", new double[]{1.0}))),
    Map.entry("nested_float_to_boolean", Map.ofEntries(Map.entry("value", new boolean[]{false}))),
    Map.entry("nested_value_types_changed", Map.ofEntries(Map.entry("value", Map.ofEntries(Map.entry("nested", new Object[]{true, 0}))))),
    Map.entry("nested_value_types_reversed", Map.ofEntries(Map.entry("value", Map.ofEntries(Map.entry("nested", new Object[]{1, false}))))),
    Map.entry("array_order_changed", Map.ofEntries(Map.entry("value", new int[]{2, 1}))),
    Map.entry("array_length_changed", Map.ofEntries(Map.entry("value", new int[]{1, 2}))),
    Map.entry("null_to_zero", Map.ofEntries(Map.entry("value", 0))),
    Map.entry("string_to_boolean", Map.ofEntries(Map.entry("value", true))),
    Map.entry("object_key_changed", Map.ofEntries(Map.entry("value", Map.ofEntries(Map.entry("b", 1)))))
);
    }
}
