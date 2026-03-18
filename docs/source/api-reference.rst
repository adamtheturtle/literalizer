API Reference
=============

.. automodule:: literalizer
   :undoc-members:
   :members:

Haskell
-------

The :data:`HASKELL` spec generates output using custom constructors
(``HNull``, ``HBool``, ``HList``, ``HMap``, ``HSet``) that are **not**
built-in Haskell types.  To compile the generated code, define a ``Val``
ADT and typeclass instances in the consuming module:

.. code-block:: haskell

   {-# LANGUAGE OverloadedStrings #-}

   import Data.String (IsString(fromString))

   data Val
     = HNull
     | HBool Bool
     | HInt Integer
     | HFloat Double
     | HStr String
     | HList [Val]
     | HMap [(String, Val)]
     | HSet [Val]

   instance IsString Val where
       fromString = HStr

   instance Num Val where
       fromInteger = HInt
       negate (HInt n)   = HInt (negate n)
       negate (HFloat f) = HFloat (negate f)
       ...

   instance Fractional Val where
       fromRational r = HFloat (realToFrac r)
       ...

``OverloadedStrings`` lets bare string literals like ``"hi"`` resolve to
``HStr "hi"`` via ``IsString``, and the ``Num`` / ``Fractional`` instances
let numeric literals resolve to ``HInt`` / ``HFloat``.

R
-

The :data:`R` spec represents dicts as named ``list()`` calls where each
entry is written as ``"key" = value``.  R's parser rejects zero-length
names, so **dict keys that are empty strings are emitted as positional
(unnamed) list elements** rather than as ``"" = value``.  The name is
lost in the output; if you need to round-trip empty-string keys, use a
different target language.
