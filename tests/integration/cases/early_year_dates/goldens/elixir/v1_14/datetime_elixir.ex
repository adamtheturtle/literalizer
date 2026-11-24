defmodule Check do
  def x do
    my_data = %{
        "date" => ~D[0099-05-27],
        "naive" => ~N[0001-01-01 12:30:00],
        "recent" => ~N[2024-05-27 10:00:00],
    }
    _ = my_data
  end
end
