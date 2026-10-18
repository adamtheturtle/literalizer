defmodule Check do
  def x do
    my_data = %{
        "minimum" => -0x80000000,
        "below" => -0xb2d05e00,
    }
    _ = my_data
  end
end
