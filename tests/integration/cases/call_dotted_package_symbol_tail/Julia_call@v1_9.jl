struct HelperType; list; end
helper = HelperType((args...; kwargs...) -> nothing)
helper.list(a=1)
