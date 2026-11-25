const WorkerType_ = struct { fn process(self__: WorkerType_, self: anytype, self_: anytype) void { _ = self__; _ = self; _ = self_; } };
const ApiType_ = struct { worker: WorkerType_ = .{} };
const api: ApiType_ = .{};
pub fn main() void {
    api.worker.process(.{}, .{});
}
