import java.util.Map;
record NamedType(int id, String label, boolean enabled, int[] related_ids) {}
record Record0(String project, NamedType lead_item) {}
class Main {
    public static void main() {
var my_data = new Record0(
    "alpha",
    new NamedType(
        100,
        "first item",
        false,
        new int[]{
            102,
            103
        }
    )
);
    }
}
