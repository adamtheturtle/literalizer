defmodule Check do
  def x do
    my_data = [
        MapSet.new(),
        MapSet.new([1, 2]),
        [],
    ]
    _ = my_data
  end
end
