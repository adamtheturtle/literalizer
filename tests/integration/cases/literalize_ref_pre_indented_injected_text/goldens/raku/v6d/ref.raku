            my $shared = [
                1,
                2,
            ];
            my $other = 3;
            my $payload = '
    shared : Val
shared = RInt 99';
            my $my_data = {
                'a' => $shared,
                'b' => $other,
                'payload' => $payload,
            };
