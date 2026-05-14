with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        ABool (True),
        AFloat (1.5),
        ANull,
        AStr ("2020-01-01"),
        AStr ("2020-01-01T00:00:00+00:00"),
        AList'[]
    ];
begin
    my_data := AList'[
        ABool (True),
        AFloat (1.5),
        ANull,
        AStr ("2020-01-01"),
        AStr ("2020-01-01T00:00:00+00:00"),
        AList'[]
    ];
end Main;
