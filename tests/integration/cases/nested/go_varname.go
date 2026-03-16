package main

func main() {
my_data := map[string]any{
    "users": []any{map[string]any{"name": "Bob", "tags": []any{"admin", "user"}}, map[string]any{"name": "Carol", "tags": []any{"guest"}}},
}
_ = my_data
}
