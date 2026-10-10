using System.Collections.Generic;
record Record0(Dictionary<string, object> Values, bool Flag, long[][] DirectArrays);
class Check {
    public static void Main() {
var my_data = new Record0(
    new Dictionary<string, object> {
        ["wide"] = new object[] {
            new long[] {
                2208988800
            },
            new long[] {}
        },
        ["narrow"] = new object[] {
            new int[] {
                946684800
            }
        },
        ["negative"] = new object[] {
            new long[] {
                -2208988800
            }
        },
        ["shifted"] = new object[] {
            new long[] {
                2208988800
            }
        },
        ["mixed_width"] = new object[] {
            new int[] {
                946684800
            },
            new long[] {
                2208988800
            }
        },
        ["text"] = "preserve"
    },
    true,
    new long[][] {
        new long[] {
            2208988800
        },
        new long[] {}
    }
);
    }
}
