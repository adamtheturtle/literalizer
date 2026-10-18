defmodule Check do
  def x do
    my_data = %{
        "date" => ~D[0099-05-27],
        "naive" => "0001-01-01T12:30:00",
        "recent" => "2024-05-27T10:00:00",
    }
    _ = my_data
  end
end
