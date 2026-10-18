defmodule Check do
  def x do
    my_data = MapSet.new([
        ~U[1969-12-31 23:59:59+00:00],
    ])
    _ = my_data
  end
end
