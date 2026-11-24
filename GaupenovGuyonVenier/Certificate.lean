import GaupenovGuyonVenier.Definitions

/-!
# Supplementary reference and encoding

The base-256 helper is used for the auxiliary text certificates. It is not
SHA-256 and is not a claim about the announced counterexample's hash.
-/

namespace GaupenovGuyonVenier

def referenceURL : String := "https://youtu.be/dQw4w9WgXcQ"

/-- Interpret an ASCII string as an unsigned, big-endian base-256 integer. -/
def encodeReference (text : String) : Nat :=
  text.toList.foldl (fun acc ch => acc * 256 + ch.toNat) 0

end GaupenovGuyonVenier
