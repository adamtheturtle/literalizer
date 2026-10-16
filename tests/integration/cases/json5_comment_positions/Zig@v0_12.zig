const ZVal = union(enum) {
    nil,
    bool: bool,
    int: i64,
    uint: u64,
    float: f64,
    str: []const u8,
    arr: []const ZVal,
    map: []const ZKV,
    set: []const ZVal,
};
const ZKV = struct { key: []const u8, val: ZVal };
pub fn main() void {
    const my_data: ZVal = .{ .map = &.{
        //
        // document heading
        // before the first entry
        // after the key
        // before the value
        .{ .key = "counts", .val = .{ .arr = &.{
            // before the first item
            .{ .int = 1 },  // inline block after the comma
            // before the second item
            .{ .int = 2 },
            // trailing inside the array
        }} },  // after the nested collection
        .{ .key = "more", .val = .{ .arr = &.{
            .{ .int = 3 },
            //
            // block heading
            // block continuation
            .{ .int = 4 },  // final inline
        }} },
        // trailing inside the object
        // after the root
        // after the document
    }};
    _ = my_data;
}
