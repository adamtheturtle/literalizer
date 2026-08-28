record Record1(int Status);
record Record2(string Status);
record Record4(string Kind, bool Urgent);
record Record3(Record4 Inner);
record Record6(string Error);
record Record5(Record6 Inner);
record Record7(Record1 Holder);
record Record8(Record2 Holder);
record Record9(long[] Nums);
record Record0(Record1 Plain, Record2 Other, Record3 NestedA, Record5 NestedB, Record7 WrapA, Record8 WrapB, Record9 Wide);
class Check {
    public static void Main() {
var my_data = new Record0(
    new Record1(
        1
    ),
    new Record2(
        "ready"
    ),
    new Record3(
        new Record4(
            "add",
            true
        )
    ),
    new Record5(
        new Record6(
            "not_found"
        )
    ),
    new Record7(
        new Record1(
            2
        )
    ),
    new Record8(
        new Record2(
            "word"
        )
    ),
    new Record9(
        new long[] {
            1,
            1099511627776
        }
    )
);
    }
}
