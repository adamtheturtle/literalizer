class ApiType; def fetch(*a, **kw); end; end
class ProcessType; def api; ApiType.new; end; end
process = ProcessType.new
process.api.fetch(data: {"data" => "hello"})
process.api.fetch(data: {"data" => 42})
process.api.fetch(data: {"data" => true})
