package main

func main() {
my_data := map[string]any{
    "users": []any{map[string]any{"name": "Bob", "tags": []string{"admin", "user"}}, map[string]any{"name": "Carol", "tags": []string{"guest"}}},
}
my_data = map[string]any{
    "users": []any{map[string]any{"name": "Bob", "tags": []string{"admin", "user"}}, map[string]any{"name": "Carol", "tags": []string{"guest"}}},
}
_ = my_data
}
