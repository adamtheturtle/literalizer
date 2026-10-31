record Record0(string Name, int[] Values);
class Check {
static object? consume(object? value = null) => null;
    public static void Main() {
var item = new Record0(
    "first",
    new int[] {
        1,
        2
    }
);
consume(item);
    }
}
