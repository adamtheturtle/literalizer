record Record2(int Value);
record Record1(object?[] Items);
record Record3(string Value);
record Record0(Record1 First, Record1 Second);
class Check {
    public static void Main() {
var my_data = new Record0(
    new Record1(
        new object?[] {
            1,
            new Record2(
                2
            )
        }
    ),
    new Record1(
        new object?[] {
            1,
            new Record3(
                "s"
            )
        }
    )
);
    _ = my_data;
    }
}
