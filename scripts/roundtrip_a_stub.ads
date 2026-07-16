--  Round-trip variant of the Ada literalizer stub.
--
--  The lint-only stub (sibling ``a_stub.ads``/``a_stub.adb``) compiles
--  every Ada fixture but stores no values, which is enough for syntax
--  checking.  The round-trip script (``run_ada_roundtrip.py``) copies
--  this richer pair in as ``a_stub.ads``/``a_stub.adb`` so the same
--  literalized fixture text can be walked and re-emitted as JSON.
--
--  The shape is deliberately untagged: one ``A_Val`` private type with a
--  heap-allocated discriminated ``Payload`` carries any of NULL / BOOL /
--  INT / FLOAT / STR / ENTRY / LIST / MAP.  ``AList``, ``AMap`` and
--  ``ASet`` are subtypes of ``A_Val`` so the Ada 2022 ``Aggregate``
--  aspect attached to ``A_Val`` is shared across all three; the LIST vs
--  MAP discrimination is decided by ``Append``: the first ``AEntry``
--  item flips a freshly-emptied container into MAP mode.  An empty
--  ``AMap'[]`` therefore cannot be told apart from an empty ``AList'[]``
--  at run time, so the round-trip driver excludes the ``empty_object``
--  key from its comparison.

with Ada.Containers.Vectors;
with Ada.Strings.Unbounded;

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

   function To_JSON (V : A_Val) return String;

private

   type Kind_T is (Null_K, Bool_K, Int_K, Float_K, Str_K,
                   Entry_K, List_K, Map_K);

   type Payload;
   type Payload_Access is access Payload;

   type A_Val is record
      Data : Payload_Access := null;
   end record;

   package Val_Vectors is new Ada.Containers.Vectors
     (Index_Type   => Positive,
      Element_Type => A_Val);

   type Payload (Kind : Kind_T := Null_K) is record
      case Kind is
         when Null_K =>
            null;
         when Bool_K =>
            Bool_V : Boolean;
         when Int_K =>
            Int_V : Long_Long_Integer;
         when Float_K =>
            Float_V : Long_Float;
         when Str_K =>
            Str_V : Ada.Strings.Unbounded.Unbounded_String;
         when Entry_K =>
            Entry_Key : Ada.Strings.Unbounded.Unbounded_String;
            Entry_Val : A_Val;
         when List_K | Map_K =>
            Items : Val_Vectors.Vector;
      end case;
   end record;

   ANull : constant A_Val := (Data => null);

end A_Stub;
