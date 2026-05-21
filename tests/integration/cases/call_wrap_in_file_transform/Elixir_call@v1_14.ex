defmodule Check do
  def process(_a, _b), do: nil
  def x do
    my_data = process(1, 2)
    _ = my_data
  end
end
