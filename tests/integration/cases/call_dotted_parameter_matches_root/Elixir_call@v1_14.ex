defmodule OuterType_ do
  def inner(_outer, _n), do: nil
end
defmodule Check do
  def x do
    outer = OuterType_
    outer.inner(1, 2)
  end
end
