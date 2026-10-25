with A_Stub; use A_Stub;
procedure Main is
    procedure Inner (Outer : A_Val; N : A_Val) is begin null; end Inner;
begin
    Inner(outer => AInt (1), n => AInt (2));
end Main;
