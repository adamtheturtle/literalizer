            declare shared=(
                1
                2
            )
            declare other=3
            declare payload="
    shared : Val
shared = RInt 99"
            declare -A my_data=(
                ["a"]=shared
                ["b"]=other
                ["payload"]=payload
            )
