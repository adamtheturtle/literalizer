defmodule Check do
  def process(_a, _b, _c, _d), do: nil
  def x do
    process(1, 2, 3, 4)
    process(5, 6, 7, 8)
  end
end
