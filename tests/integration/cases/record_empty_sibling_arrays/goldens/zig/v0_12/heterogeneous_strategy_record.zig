const Record1 = struct { item: i64 };
const Record2 = struct { item: ?i64 };
const Record0 = struct { integers: []const []const Record1, nulls: []const []const Record2, nested: []const []const []const Record1, reversed: []const []const Record1 };
pub fn main() void {
    const my_data = Record0{
        .integers = &.{
            &.{},
            &.{
                Record1{
                    .item = 1,
                },
            },
        },
        .nulls = &.{
            &.{},
            &.{
                Record2{
                    .item = null,
                },
            },
        },
        .nested = &.{
            &.{
                &.{},
                &.{
                    Record1{
                        .item = 2,
                    },
                },
            },
            &.{
                &.{
                    Record1{
                        .item = 3,
                    },
                },
                &.{},
            },
        },
        .reversed = &.{
            &.{
                Record1{
                    .item = 4,
                },
            },
            &.{},
        },
    };
    _ = my_data;
}
