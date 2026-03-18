defmodule Check do
  def x do
    my_data = %{
    "key\nwith\nnewlines" => "value1",
    "key	with	tabs" => "value2",
}
    _ = my_data
  end
end
