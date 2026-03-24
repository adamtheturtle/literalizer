defmodule Check do
  def my_data do
    %{
    "key\nwith\nnewlines" => "value1",
    "key\twith\ttabs" => "value2",
    "" => "value3",
}
  end
end
