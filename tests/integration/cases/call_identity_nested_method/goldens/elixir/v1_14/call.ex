defmodule ThingType_ do
  def go(), do: nil
end
defmodule Check do
  def x do
    outer = %{thing: ThingType_}
    outer.thing.go()
  end
end
