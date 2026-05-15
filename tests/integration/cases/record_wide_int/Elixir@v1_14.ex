defmodule Check do
  def x do
    my_data = %{
        "quantity" => 1000000,
        "big" => 18446744073709551615,
        "ratio" => 2.5,
        "label" => "tag",
        "ok" => true,
    }
    _ = my_data
  end
end
