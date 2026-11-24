defmodule Check do
  def x do
    my_data = %{
        "minimum" => -0o20000000000,
        "neighbor" => -0o17777777777,
        "maximum" => 0o17777777777,
        "nested" => [-0o20000000000],
    }
    _ = my_data
  end
end
