with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("id", AInt (1)),
        AEntry ("label", AStr ("She said ""hello"", then waved")),
        AEntry ("enabled", ABool (False)),
        AEntry ("related_ids", AList'[AInt (1), AInt (2), AInt (3)])
    ];
begin
    null;
end Main;
