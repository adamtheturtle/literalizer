my_data = {
    struct('input', struct('name', "alice", 'city', "paris"), 'expected', struct('count', 1, 'total', 2)),
    struct('input', struct('name', 10, 'city', 20), 'expected', struct('count', "done", 'total', "pending"))
};
