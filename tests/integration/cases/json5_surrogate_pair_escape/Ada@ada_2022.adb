with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("astral", AStr ("😀")),
        AEntry ("mixed", AStr ("a😀b")),
        AEntry ("count", AInt (2)),
        AEntry ("list", AList'[AStr ("😀"), AInt (1)]),
        AEntry ("nested", AMap'[AEntry ("inner", AStr ("😀"))])
    ];
begin
    null;
end Main;
