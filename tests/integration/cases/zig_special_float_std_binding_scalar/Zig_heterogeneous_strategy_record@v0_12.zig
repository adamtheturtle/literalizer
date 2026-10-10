const @"literalizer float std" = @import("std");
pub fn main() void {
    const std = @"literalizer float std".math.nan(f64);
    _ = std;
}
