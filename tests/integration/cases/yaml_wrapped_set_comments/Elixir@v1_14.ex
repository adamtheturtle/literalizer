defmodule Check do
  def x do
    my_data = MapSet.new([
        10,  # comment for ten
        2,  # comment for two
    ])
    _ = my_data
  end
end
