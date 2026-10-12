record Record1(string X);
record Record2(int X);
record Record0(Record1 Direct, Record2 Bound);
class Check {
static Record2 RefData = new Record2(
    1
);
static Record0 my_data = new Record0(
    new Record1(
        "s"
    ),
    RefData
);
    public static void Main() {}
}
