defmodule Check do
  def my_data do
    my_data = %{
    "key" => "\"bang!\"",  # real
}
    _ = my_data
  end
end
