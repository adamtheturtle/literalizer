using System.Collections.Generic;
record Record0(int Id, string Description, bool IsDone, int[] Blocks);
class Check {
    public static void Main() {
var my_data = new Record0(
    1,
    "She said \"hello\", then waved",
    false,
    new int[] {
        1,
        2,
        3
    }
);
    }
}
