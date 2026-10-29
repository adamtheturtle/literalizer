with A_Stub; use A_Stub;
procedure Main is
    procedure F (Value : A_Val) is begin null; end F;
    ref_data : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
begin
    F(value => AList'[
        ref_data
    ]);
    F(value => AList'[
        ref_data
    ]);
end Main;
