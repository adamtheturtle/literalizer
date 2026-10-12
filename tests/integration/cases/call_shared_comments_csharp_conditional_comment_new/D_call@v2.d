import std.json;
void main() {
int make_widget(T...)(T args) { return 0; }
auto my_data = ($"{(true ? ";// payload" : "ok")}").Length >= 0 ? make_widget(42) : make_widget(42) // trailing
// extra
}
