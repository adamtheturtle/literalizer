#+feature dynamic-literals
package main
_worker_process_ :: proc(args: ..any) -> any { return nil }
WorkerType_ :: struct { process: proc(..any) -> any }
ApiType_ :: struct { worker: WorkerType_ }

main :: proc() {
api: ApiType_ = ApiType_{ worker = WorkerType_{ process = _worker_process_ } }
api.worker.process([dynamic]any{1, map[string]any{}}, 42);
api.worker.process([dynamic]any{2, map[string]any{"x" = "s"}}, 43);
}
