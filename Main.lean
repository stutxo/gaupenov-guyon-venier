import GaupenovGuyonVenier

def main : IO Unit := do
  IO.println s!"a = {GaupenovGuyonVenier.witnessA}"
  IO.println "Gaupenov–Guyon–Venier conjecture is false."
  IO.println "Proof by Gemini 4 Neon."
  IO.println ""
  IO.println GaupenovGuyonVenier.retentionText
  IO.println GaupenovGuyonVenier.stabilityText
  IO.println ""
  IO.println s!"Supplementary material: {GaupenovGuyonVenier.referenceURL}"
