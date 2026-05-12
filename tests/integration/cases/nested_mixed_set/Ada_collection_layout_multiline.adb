with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("name", AStr ("Alice")),
        AEntry ("tags", ASet'[
            ABool (True),
            AInt (42),
            AStr ("apple")
        ])
    ];
begin
    null;
end Main;
