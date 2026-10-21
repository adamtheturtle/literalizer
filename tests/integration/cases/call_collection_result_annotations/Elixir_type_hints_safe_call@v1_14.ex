defmodule Check do
  def make_widget(_items), do: nil
  def x do
    my_data = make_widget([[1, 2], [3]])
    _ = my_data
  end
end
