#+feature dynamic-literals
package main
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
make_widget([dynamic]any{}, [dynamic]any{1}, [dynamic]any{});
make_widget([dynamic]any{"text"}, [dynamic]any{2}, [dynamic]any{});
make_widget([dynamic]any{}, [dynamic]any{"text"}, [dynamic]any{});
make_widget([dynamic]any{"text"}, [dynamic]any{2}, [dynamic]any{3});
}
