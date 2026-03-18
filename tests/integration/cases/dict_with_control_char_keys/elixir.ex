defmodule Check do
  def x do
    %{
    "key\nwith\nnewlines" => "value1",
    "key	with	tabs" => "value2",
}
  end
end
