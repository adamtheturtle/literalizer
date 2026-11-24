defmodule Check do
  def x do
    my_data = %{
        "below" => -2147483649,
        "minimum" => -2147483648,
        "above" => -2147483647,
        "nested" => [0],
    }
    _ = my_data
  end
end
