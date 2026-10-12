function make_widget(...) end
local my_data = ("\"prefix ${"// payload"}\"").length >= 0 ? make_widget(42) : make_widget(42) // trailing
// extra
