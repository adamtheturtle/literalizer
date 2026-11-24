defmodule Check do
  def x do
    my_data = %{
        "below" => -0o20000000001,
        "minimum" => -0o20000000000,
        "above" => -0o17777777777,
        "nested" => [0o0],
    }
    _ = my_data
  end
end
