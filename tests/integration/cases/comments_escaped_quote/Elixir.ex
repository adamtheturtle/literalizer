defmodule Check do
  def my_data do
    %{
    "key" => "value \" # not a comment",  # real
}
  end
end
