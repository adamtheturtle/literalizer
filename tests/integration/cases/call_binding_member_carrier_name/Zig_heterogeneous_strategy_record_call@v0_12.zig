const ObjType_ = struct { fn ZVal(self: ObjType_, _arg: anytype) i64 { _ = self; _ = _arg; return 0; } };
const obj: ObjType_ = .{};
pub fn main() void {
    const my_data = obj.ZVal(42); // note
    _ = my_data;
}
