with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("s", AStr ("string")),
        AEntry ("i", AInt (1)),
        AEntry ("f", AFloat (1.5)),
        AEntry ("b", ABool (True)),
        AEntry ("n", ANull),
        AEntry ("d", AStr ("2024-01-15")),
        AEntry ("dt", AStr ("2024-01-15T12:00:00")),
        AEntry ("by", AStr ("48656c6c6f"))
    ];
begin
    null;
end Main;
