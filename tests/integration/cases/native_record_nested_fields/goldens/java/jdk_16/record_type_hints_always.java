record Record1(String name, boolean active) {}
record Record2(String name, double score) {}
record Record0(Record1 owner, Record2[] members) {}
class Main {
    public static void main() {
Record0 my_data = new Record0(
    new Record1(
        "Ada",
        false
    ),
    new Record2[]{
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
    }
}
