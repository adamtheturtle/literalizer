defmodule ThingType_ do
  def first_value(_value), do: nil
end
defmodule Check do
  def x do
    thing = ThingType_
    thing.first_value(1)
  end
end
