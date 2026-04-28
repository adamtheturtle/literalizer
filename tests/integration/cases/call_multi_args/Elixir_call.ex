defmodule Check do
  def process(_value, _count), do: nil
  def x do
    process(1, 42)
    process(2, 100)
  end
end
