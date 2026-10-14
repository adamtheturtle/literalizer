defmodule Http_clientType_ do
  def fetch(_payload), do: nil
end
defmodule Check do
  def x do
    my_app = %{http_client: Http_clientType_}
    my_app.http_client.fetch("hello")
    my_app.http_client.fetch(42)
    my_app.http_client.fetch(true)
  end
end
