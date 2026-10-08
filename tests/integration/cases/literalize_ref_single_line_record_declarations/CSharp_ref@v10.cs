record Record1(string X);
record Record2(int X);
record Record0(Record1 Direct, Record2 Bound);
class Check {
    public static void Main() {
var First = new Record2(
    1
);
var my_data = new Record0(
    new Record1(
        "s"
    ),
    First
);
    }
}
