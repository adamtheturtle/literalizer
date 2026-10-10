const ObjType_ = struct { fn ZVal(self: ObjType_, value: anytype) void { _ = self; _ = value; } };
const obj: ObjType_ = .{};
pub fn main() void {
    obj.ZVal(1);
}
