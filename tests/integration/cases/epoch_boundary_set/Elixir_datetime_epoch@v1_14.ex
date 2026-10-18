defmodule Check do
  def x do
    my_data = MapSet.new([
        -2147483649,
        -2147483648,
        2147483647,
        2147483648,
    ])
    _ = my_data
  end
end
