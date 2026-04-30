defmodule Check do
  def x do
    ref_x = %{
        "_" => "_",
    }
    my_data = [
        ref_x,
        1,
        2,
    ]
    _ = my_data
  end
end
