defmodule Check do
  def x do
    my_data = %{
        "minimum" => -0b10000000000000000000000000000000,
        "neighbor" => -0b1111111111111111111111111111111,
        "maximum" => 0b1111111111111111111111111111111,
        "nested" => [-0b10000000000000000000000000000000],
    }
    _ = my_data
  end
end
