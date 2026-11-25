defmodule ThingType_ do
  def go(_value), do: nil
end
defmodule Check do
  def x do
    thing = ThingType_
    my_data = thing.go([1])
    _ = my_data
  end
end
