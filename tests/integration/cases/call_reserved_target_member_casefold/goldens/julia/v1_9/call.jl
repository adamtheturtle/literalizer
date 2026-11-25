struct ObjType; BEGIN; end
obj = ObjType((args...; kwargs...) -> nothing)
obj.BEGIN(a=42)
