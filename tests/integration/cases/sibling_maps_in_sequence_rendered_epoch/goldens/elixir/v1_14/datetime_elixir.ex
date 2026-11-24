defmodule Check do
  def x do
    my_data = [
        %{"k" => ~U[2040-01-01 00:00:00+00:00]},
        %{"k" => 1},
    ]
    _ = my_data
  end
end
