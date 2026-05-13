defmodule Check do
  def x do
    my_data = MapSet.new([
        1,
        1099511627776,
    ])
    _ = my_data
  end
end
