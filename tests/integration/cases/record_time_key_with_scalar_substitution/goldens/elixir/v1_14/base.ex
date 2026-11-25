defmodule Check do
  def x do
    my_data = %{
        "value" => %{"01:02:03" => 1},
        "other" => 2,
    }
    _ = my_data
  end
end
