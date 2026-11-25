record Record0(int DueDate, int ParentId, string Assignee);
class Check {
    public static void Main() {
var my_data = new[] {
    new Record0(-1, -1, ""),
    new Record0(10, 20, "alice")
};
    _ = my_data;
    }
}
