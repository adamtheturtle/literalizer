#+feature dynamic-literals
package main
_app_go_ :: proc(args: ..any) -> any { return nil }
AppType_ :: struct { go: proc(..any) -> any }

main :: proc() {
app: AppType_ = AppType_{ go = _app_go_ }
app.go([dynamic]any{1}, [dynamic]any{"text"});
}
