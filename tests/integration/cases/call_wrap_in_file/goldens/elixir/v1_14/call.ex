defmodule Check do
  def process(_a, _b), do: nil
  def x do
    process(1, 2)
    process(3, 4)
  end
end
