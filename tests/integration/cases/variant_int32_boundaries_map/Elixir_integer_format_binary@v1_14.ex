defmodule Check do
  def x do
    my_data = %{
        "below" => -0b10000000000000000000000000000001,
        "minimum" => -0b10000000000000000000000000000000,
        "above" => -0b1111111111111111111111111111111,
        "nested" => [0b0],
    }
    _ = my_data
  end
end
