            $Shared = @(
                1;
                2
            )
            $Other = 3
            $Payload = "`n    shared : Val`nshared = RInt 99"
            $my_data = @{
                "a" = $Shared;
                "b" = $Other;
                "payload" = $Payload
            }
