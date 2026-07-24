import java.util.Map;
record NamedType(int id, String label, boolean enabled, int[] related_ids) {}
record Record0(String collection, NamedType featured_entry) {}
class Main {
    public static void main() {
var my_data = new Record0(
    "alpha",
    new NamedType(
        100,
        "first entry",
        false,
        new int[]{
            102,
            103
        }
    )
);
    }
}
