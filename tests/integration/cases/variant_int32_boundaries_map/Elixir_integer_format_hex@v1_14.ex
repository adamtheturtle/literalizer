defmodule Check do
  def x do
    my_data = %{
        "below" => -0x80000001,
        "minimum" => -0x80000000,
        "above" => -0x7fffffff,
        "nested" => [0x0],
    }
    _ = my_data
  end
end
