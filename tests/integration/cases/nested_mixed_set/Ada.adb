with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("name", AStr ("Alice")),
        AEntry ("tags", ASet'[ABool (True), AInt (42), AStr ("apple")])
    ];
begin
    null;
end Check;
