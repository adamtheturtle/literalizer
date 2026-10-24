defmodule Check do
  def x do
    my_data = %{
        "date" => ~D[0099-05-27],
        "naive" => -62135551800,
        "recent" => 1716804000,
    }
    _ = my_data
  end
end
