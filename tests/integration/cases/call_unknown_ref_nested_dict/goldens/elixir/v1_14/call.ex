defmodule Check do
  def process(_data), do: nil
  def x do
    my_list = %{
        "unused" => "value",
    }
    process([[%{"inner" => my_list}]])
  end
end
