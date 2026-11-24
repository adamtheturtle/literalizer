defmodule Check do
  def x do
    my_data = %{
        "b" => %{"k" => 1},
        "a" => %{"k" => ~U[2040-01-01 00:00:00+00:00]},
    }
    _ = my_data
  end
end
