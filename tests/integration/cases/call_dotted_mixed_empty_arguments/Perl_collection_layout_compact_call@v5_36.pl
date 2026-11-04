sub thing {}
sub go {}
thing.go([], [1], []);
thing.go(["text"], [2], []);
thing.go([], ["text"], []);
thing.go(["text"], [2], [3]);
