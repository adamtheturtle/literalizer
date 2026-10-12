make_widget(args...; kwargs...) = nothing
my_data = ("${"${"// payload"}"}").length >= 0 ? make_widget(count=42) : make_widget(count=42) // trailing
// extra
