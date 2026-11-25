defmodule ThingType_ do
  def go(), do: nil
end
defmodule Check do
  def x do
    thing = ThingType_
    thing.go()
  end
end
