const Record1 = struct { status: i64 };
const Record2 = struct { status: []const u8 };
const Record4 = struct { kind: []const u8, urgent: bool };
const Record3 = struct { inner: Record4 };
const Record6 = struct { @"error": []const u8 };
const Record5 = struct { inner: Record6 };
const Record7 = struct { holder: Record1 };
const Record8 = struct { holder: Record2 };
const Record9 = struct { nums: []const i64 };
const Record0 = struct { plain: Record1, other: Record2, nested_a: Record3, nested_b: Record5, wrap_a: Record7, wrap_b: Record8, wide: Record9 };
pub fn main() void {
    const my_data = Record0{
        .plain = Record1{
            .status = 1,
        },
        .other = Record2{
            .status = "ready",
        },
        .nested_a = Record3{
            .inner = Record4{
                .kind = "add",
                .urgent = true,
            },
        },
        .nested_b = Record5{
            .inner = Record6{
                .@"error" = "not_found",
            },
        },
        .wrap_a = Record7{
            .holder = Record1{
                .status = 2,
            },
        },
        .wrap_b = Record8{
            .holder = Record2{
                .status = "word",
            },
        },
        .wide = Record9{
            .nums = &.{
                1,
                1099511627776,
            },
        },
    };
    _ = my_data;
}
