            shared = {
                1,
                2
            };
            other = 3;
            payload = sprintf('%s%s%s%s', char(10), "    shared : Val", char(10), "shared = RInt 99");
            my_data = struct(
                'a', shared,
                'b', other,
                'payload', payload
            );
