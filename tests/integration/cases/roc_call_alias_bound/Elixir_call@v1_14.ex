defmodule Check do
  def process(_value), do: nil
  def x do
    my_data = process(1)
    _ = my_data
  end
end
