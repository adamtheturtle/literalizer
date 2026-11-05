record Record1(int A);
record Record0(Record1[] Items);
class Check {
    public static void Main() {
var my_data = new Record0(
    new[] {
        new Record1(
            1
        )
    }
);
    _ = my_data;
    }
}
