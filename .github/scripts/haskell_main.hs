-- Driver template used by the ``Lint Haskell`` job in
-- ``.github/workflows/lint.yml``. The placeholder ``MODULE_PLACEHOLDER``
-- is replaced with the per-fixture module name (deterministic
-- ``Fixture_<dir>_<stem>`` derived from the golden's path) before
-- being handed to ghc, so the wrapper forces the fixture's
-- ``my_data`` value to evaluate.
module Main where

import qualified MODULE_PLACEHOLDER as F

main :: IO ()
main = seq F.my_data (return ())
