defmodule ThingType_ do
  def go(), do: nil
end
defmodule OuterType_ do
  def thing, do: ThingType_
end
defmodule Check do
  def x do
    outer = OuterType_
    outer.thing.go()
  end
end
