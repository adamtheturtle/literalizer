with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("id", AInt (1)),
        AEntry ("description", AStr ("She said ""hello"", then waved")),
        AEntry ("is_done", ABool (False)),
        AEntry ("blocks", AList'[AInt (1), AInt (2), AInt (3)])
    ];
begin
    my_data := AMap'[
        AEntry ("id", AInt (1)),
        AEntry ("description", AStr ("She said ""hello"", then waved")),
        AEntry ("is_done", ABool (False)),
        AEntry ("blocks", AList'[AInt (1), AInt (2), AInt (3)])
    ];
end Main;
