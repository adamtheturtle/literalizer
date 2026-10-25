#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"below" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{1}}}}}}}},
	"boundary" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{2}}}}}}}}},
	"multiple" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{3}}}}}}}}}}}}}}}}},
	"text" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{"value"}}}}}}}}},
	"boolean" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{true}}}}}}}}},
	"float" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{1.5}}}}}}}}},
}
my_data = map[string]any{
	"below" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{1}}}}}}}},
	"boundary" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{2}}}}}}}}},
	"multiple" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{3}}}}}}}}}}}}}}}}},
	"text" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{"value"}}}}}}}}},
	"boolean" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{true}}}}}}}}},
	"float" = [dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{[dynamic]any{1.5}}}}}}}}},
}
_ = my_data
}
