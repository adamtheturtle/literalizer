defmodule Check do
  def x do
    %{
    "key" => "value \" # not a comment",  # real
}
  end
end
