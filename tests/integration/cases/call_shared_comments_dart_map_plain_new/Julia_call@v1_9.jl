make_widget(args...; kwargs...) = nothing
my_data = ("${{'value': '// payload'}['value']}").length >= 0 ? make_widget(count=42) : make_widget(count=42)
