import GaupenovGuyonVenier.Definitions

/-!
# Stability lemma

No iterate falls below the initial value. Stationarity would otherwise
give a strict inequality from an integer to itself.
-/

namespace GaupenovGuyonVenier

theorem never_gonna_let_you_down (initial : Int) : ¬ Descent initial := by
  intro h
  cases h with
  | intro n hn =>
    rw [orbit_stationary initial n] at hn
    exact (Int.lt_irrefl initial) hn

end GaupenovGuyonVenier
