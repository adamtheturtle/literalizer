with A_Stub; use A_Stub;
procedure Main is
    procedure Process (A : A_Val; B : A_Val) is begin null; end Process;
    big_list : A_Val := AList'[
        AStr ("x")
    ];
begin
    Process(a => AMap'[AEntry ("k", big_list)], b => AMap'[AEntry ("m", big_list)]);
end Main;
