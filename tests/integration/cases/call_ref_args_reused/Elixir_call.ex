defmodule Check do
  def process(_data, _count), do: nil
  def x do
    shared = 1
    other = 2
    process(shared, 1)
    process(other, 0)
    process(shared, 8)
  end
end
