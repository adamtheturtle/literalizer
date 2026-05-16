import java.util.Map;
record Task(int id, String description, boolean is_done, int[] blocks) {}
record Record0(String project, Task lead_task) {}
class Module {
    public static void module() {
var my_data = new Record0(
    "alpha",
    new Task(
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
