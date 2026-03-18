defmodule Check do
  def x do
    %{
    "key\nwith\nnewlines" => "value1",
    "key\twith\ttabs" => "value2",
}
  end
end
