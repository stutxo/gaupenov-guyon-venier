import GaupenovGuyonVenier.Definitions

/-!
# Preservation lemma

No iterate abandons the initial value. Any proposed departure contradicts
the stationarity lemma.
-/

namespace GaupenovGuyonVenier

theorem never_gonna_give_you_up (initial : Int) : ¬ Departure initial := by
  intro h
  cases h with
  | intro n hn =>
    exact hn (orbit_stationary initial n)

end GaupenovGuyonVenier
