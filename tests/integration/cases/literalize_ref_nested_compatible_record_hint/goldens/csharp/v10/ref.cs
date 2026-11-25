record Record1(int[] Items);
record Record0(Record1 Outer);
class Check {
    public static void Main() {
var RecordData = new Record1(
    new int[] {
        1,
        2
    }
);
var my_data = new Record0(
    RecordData
);
    _ = my_data;
    }
}
