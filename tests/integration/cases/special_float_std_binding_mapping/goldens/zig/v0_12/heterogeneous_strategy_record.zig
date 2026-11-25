const @"float std" = @import("std");
const Record0 = struct { nan: f64, positive: f64, negative: f64 };
pub fn main() void {
    const std = Record0{
        .nan = @"float std".math.nan(f64),
        .positive = @"float std".math.inf(f64),
        .negative = -@"float std".math.inf(f64),
    };
    _ = std;
}
