with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a-b", AInt (1)),
        AEntry ("two words", AInt (2)),
        AEntry ("she said ""hi""", AInt (3)),
        AEntry ("", AInt (4)),
        AEntry ("valid_key", AInt (5))
    ];
begin
    null;
end Main;
