with A_Stub; use A_Stub;
procedure Main is
    procedure Consume (Items : A_Val; Mapping : A_Val) is begin null; end Consume;
    foo : A_Val := AInt (42);
begin
    Consume(items => AList'[
        AMap'[
            AEntry ("other", AInt (1))
        ],
        foo
    ], mapping => AMap'[
        AEntry ("left", foo),
        AEntry ("other", AInt (1))
    ]);
end Main;
