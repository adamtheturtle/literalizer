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
const PlaylistType_ = struct { fn newValue(self: PlaylistType_, x: ZVal) void { _ = self; _ = x; } };
const Playlist: PlaylistType_ = .{};
pub fn main() void {
    Playlist.newValue(.{ .int = 1 });
}
