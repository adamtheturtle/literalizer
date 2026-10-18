defmodule Check do
  def x do
    my_data = [
        ~N[1901-12-13 20:45:51],
        ~N[1901-12-13 20:45:52],
        ~N[2038-01-19 03:14:07],
        ~N[2038-01-19 03:14:08],
    ]
    _ = my_data
  end
end
