struct ObjType; ZVal; end
obj = ObjType((args...; kwargs...) -> nothing)
my_data = obj.ZVal(_arg=42) // note
