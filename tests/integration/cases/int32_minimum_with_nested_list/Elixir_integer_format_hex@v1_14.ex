defmodule Check do
  def x do
    my_data = %{
        "minimum" => -0x80000000,
        "neighbor" => -0x7fffffff,
        "maximum" => 0x7fffffff,
        "nested" => [-0x80000000],
    }
    _ = my_data
  end
end
