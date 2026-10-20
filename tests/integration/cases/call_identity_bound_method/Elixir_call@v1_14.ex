defmodule ThingType_ do
  def go(_value), do: nil
end
defmodule Check do
  def x do
    thing = ThingType_
    item = [
        1,
        2,
    ]
    thing.go(item)
  end
end
