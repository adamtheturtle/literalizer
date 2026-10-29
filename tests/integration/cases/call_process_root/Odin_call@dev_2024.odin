#+feature dynamic-literals
package main
_api_fetch_ :: proc(args: ..any) -> any { return nil }
ApiType_ :: struct { fetch: proc(..any) -> any }
ProcessType_ :: struct { api: ApiType_ }

main :: proc() {
process: ProcessType_ = ProcessType_{ api = ApiType_{ fetch = _api_fetch_ } }
process.api.fetch(map[string]any{"data" = "hello"});
process.api.fetch(map[string]any{"data" = 42});
process.api.fetch(map[string]any{"data" = true});
}
