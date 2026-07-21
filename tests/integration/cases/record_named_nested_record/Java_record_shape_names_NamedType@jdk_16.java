import java.util.Map;
record NamedType(int id, String description, boolean is_done, int[] blocks) {}
record Record0(String project, NamedType lead_task) {}
class Main {
    public static void main() {
var my_data = new Record0(
    "alpha",
    new NamedType(
        100,
        "first task",
        false,
        new int[]{
            102,
            103
        }
    )
);
    }
}
