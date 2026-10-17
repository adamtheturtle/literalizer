struct AppType; go; end
app = AppType((args...; kwargs...) -> nothing)
app.go(first_value=[1], second_value=["text"])
