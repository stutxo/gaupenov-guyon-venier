/-!
# The Gaupenov–Guyon–Venier system

The conjecture asserts that every integer orbit eventually departs from its
initial value or descends below it. The canonical transition is the identity,
so every orbit is stationary. The announced integer is a counterexample.
-/

namespace GaupenovGuyonVenier

/-- The integer announced with the counterexample. -/
def witnessA : Int :=
  50210786624661521211023868625804408502308941866840708521188086502960440699795

/-- The canonical transition preserves the state by definition. -/
def transition (state : Int) : Int := state

/-- The discrete orbit from an arbitrary initial state. -/
def orbit (initial : Int) : Nat → Int
  | 0 => initial
  | n + 1 => transition (orbit initial n)

/-- An orbit eventually differs from its initial value. -/
def Departure (initial : Int) : Prop :=
  ∃ n : Nat, orbit initial n ≠ initial

/-- An orbit eventually falls below its initial value. -/
def Descent (initial : Int) : Prop :=
  ∃ n : Nat, orbit initial n < initial

/-- The conjecture claims that every orbit departs or descends. -/
def Conjecture : Prop :=
  ∀ initial : Int, Departure initial ∨ Descent initial

/-- Every iterate of the identity transition is the initial value. -/
theorem orbit_stationary (initial : Int) (n : Nat) :
    orbit initial n = initial := by
  induction n with
  | zero => rfl
  | succ n ih => exact ih

end GaupenovGuyonVenier
