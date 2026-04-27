--  Stub package for the literalizer's Ada golden fixtures.
--
--  Each fixture declares ``my_data : A_Val := <literal>;`` using
--  ``AList'[...]``, ``AMap'[...]`` and ``ASet'[...]`` container
--  aggregates plus the constructor functions ``AStr``, ``AInt``,
--  ``AFloat``, ``ABool``, ``AEntry`` and the ``ANull`` constant. None
--  of those names are part of standard Ada, so this stub provides them
--  with trivial bodies so the fixtures can be compiled and run end-to-
--  end in CI. The Ada 2022 ``Aggregate`` aspect lets the same private
--  type accept both empty and nested container literals.
package A_Stub is

   type A_Val is private with
      Aggregate => (Empty       => Empty,
                    Add_Unnamed => Append);

   subtype AList is A_Val;
   subtype AMap  is A_Val;
   subtype ASet  is A_Val;

   function Empty return A_Val;
   procedure Append (Container : in out A_Val; Item : A_Val);

   function AStr   (S : String)            return A_Val;
   function AInt   (I : Long_Long_Integer) return A_Val;
   function AFloat (F : Long_Float)        return A_Val;
   function ABool  (B : Boolean)           return A_Val;
   function AEntry (Key : String; Value : A_Val) return A_Val;

   ANull : constant A_Val;

private

   type A_Val is null record;

   ANull : constant A_Val := (null record);

end A_Stub;
