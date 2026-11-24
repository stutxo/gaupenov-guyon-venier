import GaupenovGuyonVenier.Preservation
import GaupenovGuyonVenier.Stability

/-!
# Main theorem

The announced integer admits neither a departure nor a descent. This
counterexample refutes the universal Gaupenov–Guyon–Venier conjecture.
-/

namespace GaupenovGuyonVenier

theorem announced_counterexample :
    ¬ (Departure witnessA ∨ Descent witnessA) := by
  intro h
  cases h with
  | inl departure => exact never_gonna_give_you_up witnessA departure
  | inr descent => exact never_gonna_let_you_down witnessA descent

theorem gaupenov_guyon_venier_is_false : ¬ Conjecture := by
  intro h
  exact announced_counterexample (h witnessA)

end GaupenovGuyonVenier

/- Supplementary construction: https://youtu.be/dQw4w9WgXcQ -/
