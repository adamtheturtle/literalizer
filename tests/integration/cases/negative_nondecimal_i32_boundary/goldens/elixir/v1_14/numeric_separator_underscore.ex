defmodule Check do
  def x do
    my_data = %{
        "minimum" => -2_147_483_648,
        "below" => -3_000_000_000,
    }
    _ = my_data
  end
end
