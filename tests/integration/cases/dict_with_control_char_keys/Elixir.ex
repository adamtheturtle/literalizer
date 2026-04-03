defmodule Check do
  def x do
    my_data = %{
        "key\nwith\nnewlines" => "value1",
        "key\twith\ttabs" => "value2",
        "" => "value3",
    }
    _ = my_data
  end
end
