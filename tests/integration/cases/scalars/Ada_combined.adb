with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AInt (42),
        AFloat (3.14),
        ABool (True),
        ABool (False),
        AStr ("hello ""world""")
    ];
begin
    my_data := AList'[
        AInt (42),
        AFloat (3.14),
        ABool (True),
        ABool (False),
        AStr ("hello ""world""")
    ];
end Check;
