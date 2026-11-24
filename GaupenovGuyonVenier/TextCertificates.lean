import GaupenovGuyonVenier.Certificate

/-!
# Text certificates

The two auxiliary constants are exact base-256 encodings of the short
textual witnesses. The kernel checks both encodings by reduction.
-/

namespace GaupenovGuyonVenier

def retentionText : String := "never gonna give you up"

def stabilityText : String := "never gonna let you down"

def retentionCode : Nat :=
  10573868466134194369802649438521576810613097274607170928

def stabilityCode : Nat :=
  2706910327330353758669478256263066242151633179653857834862

theorem retention_text_certificate :
    encodeReference retentionText = retentionCode := by
  decide

theorem stability_text_certificate :
    encodeReference stabilityText = stabilityCode := by
  decide

end GaupenovGuyonVenier
