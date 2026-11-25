defmodule Check do
  def x do
    my_data = [
        "prefix ${HOME} suffix",
        "${interpolated}",
    ]
    _ = my_data
  end
end
