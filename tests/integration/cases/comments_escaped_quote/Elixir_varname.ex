defmodule Check do
  def my_data do
    my_data = %{
    "key" => "value \" # not a comment",  # real
}
    _ = my_data
  end
end
