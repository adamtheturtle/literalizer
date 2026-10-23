#+feature dynamic-literals
package main
_process_fetch_ :: proc(args: ..any) -> any { return nil }
ProcessType_ :: struct { fetch: proc(..any) -> any }
AppType_ :: struct { process: ProcessType_ }

main :: proc() {
app: AppType_ = AppType_{ process = ProcessType_{ fetch = _process_fetch_ } }
app.process.fetch(map[string]any{"data" = "hello"});
app.process.fetch(map[string]any{"data" = 42});
app.process.fetch(map[string]any{"data" = true});
}
