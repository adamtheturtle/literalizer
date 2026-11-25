defmodule Check do
  def x do
    my_data = MapSet.new([
        "1901-12-13T20:45:51",
        "1901-12-13T20:45:52",
        "2038-01-19T03:14:07",
        "2038-01-19T03:14:08",
    ])
    _ = my_data
  end
end
