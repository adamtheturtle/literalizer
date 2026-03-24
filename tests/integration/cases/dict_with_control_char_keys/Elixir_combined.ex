defmodule Check do
  def my_data do
    my_data = %{
    "key\nwith\nnewlines" => "value1",
    "key\twith\ttabs" => "value2",
    "" => "value3",
}
    _ = my_data
  end
end
