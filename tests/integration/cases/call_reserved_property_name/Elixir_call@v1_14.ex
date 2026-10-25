defmodule FooType_ do
  def class(_value), do: nil
end
defmodule Check do
  def x do
    foo = FooType_
    foo.class(1)
  end
end
