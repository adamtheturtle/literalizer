my_data = [
    Dict("input" => Dict("name" => "alice", "city" => "paris"), "expected" => Dict("count" => 1, "total" => 2)),
    Dict("input" => Dict("name" => 10, "city" => 20), "expected" => Dict("count" => "done", "total" => "pending")),
]
