process(args...; kwargs...) = nothing
struct HelpersType; emit; end
helpers = HelpersType((args...; kwargs...) -> nothing)
helpers.emit(process(value=1), 42)
