record Record1(string Name, bool Active);
record Record2(string Name, double Score);
record Record0(Record1 Owner, Record2[] Members);
class Check {
    public static void Main() {
var my_data = new Record0(
    new Record1(
        "Ada",
        false
    ),
    new[] {
        new Record2(
            "Ada",
            1.5
        ),
        new Record2(
            "Bob",
            2.5
        )
    }
);
    _ = my_data;
    }
}
