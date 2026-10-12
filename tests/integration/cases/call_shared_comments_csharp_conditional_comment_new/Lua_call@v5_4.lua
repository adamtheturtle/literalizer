function make_widget(...) end
local my_data = ($"{(true ? "// payload" : "ok")}").Length >= 0 ? make_widget(42) : make_widget(42) // trailing
// extra
