defmodule Check do
  def x do
    my_data = %{
        "minimum" => -0b10000000000000000000000000000000,
        "below" => -0b10110010110100000101111000000000,
    }
    _ = my_data
  end
end
