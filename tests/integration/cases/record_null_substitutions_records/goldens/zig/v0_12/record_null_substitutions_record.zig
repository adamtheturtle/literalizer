const Record0 = struct { due_date: i64, parent_id: i64, assignee: []const u8 };
pub fn main() void {
    const my_data = &.{
        Record0{ .due_date = -1, .parent_id = -1, .assignee = "" },
        Record0{ .due_date = 10, .parent_id = 20, .assignee = "alice" },
    };
    _ = my_data;
}
