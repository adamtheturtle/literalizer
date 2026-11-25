defmodule ObjType_ do
  def class(_a), do: nil
end
defmodule Check do
  def x do
    obj = ObjType_
    obj.class(42)
  end
end
