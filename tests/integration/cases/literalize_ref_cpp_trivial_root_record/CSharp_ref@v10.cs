record Record1(int Value);
record Record0(Record1 Child);
class Check {
    public static void Main() {
var First = new Record0(
    new Record1(
        1
    )
);
var my_data = First;
    }
}
