make_widget(args...; kwargs...) = nothing
my_data = make_widget(count=42) ?
make_widget(count=42) // inner
: nil // trailing
