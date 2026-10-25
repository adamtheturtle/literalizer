#+feature dynamic-literals
package main
_api_process_ :: proc(args: ..any) -> any { return nil }
ApiType_ :: struct { process: proc(..any) -> any }

main :: proc() {
api: ApiType_ = ApiType_{ process = _api_process_ }
api.process(map[string]any{});
}
