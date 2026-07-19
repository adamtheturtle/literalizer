import java.util.Map;
record Record1(int status) {}
record Record2(String status) {}
record Record4(String kind, boolean urgent) {}
record Record3(Record4 inner) {}
record Record6(String error) {}
record Record5(Record6 inner) {}
record Record7(Record1 holder) {}
record Record8(Record2 holder) {}
record Record9(long[] nums) {}
record Record0(Record1 plain, Record2 other, Record3 nested_a, Record5 nested_b, Record7 wrap_a, Record8 wrap_b, Record9 wide) {}
class Main {
    public static void main() {
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
        new long[]{
            1L,
            1099511627776L
        }
    )
);
    }
}
