# Gaupenov–Guyon–Venier

A Lean 4 counterexample to the Gaupenov–Guyon–Venier conjecture.

```text
a = 50210786624661521211023868625804408502308941866840708521188086502960440699795

Gaupenov–Guyon–Venier conjecture is false

Proof by Gemini 4 Neon
```

## Formal proof

The argument proceeds by persistence, exclusion of strict descent, and
specialization to the announced integer.

**[Read the complete proof →](GaupenovGuyonVenier/Proof.lean)**

[▶ Watch the proof walkthrough](https://youtu.be/dQw4w9WgXcQ)

[Read the white paper (PDF) →](paper/gaupenov_guyon_venier_whitepaper.pdf)

| Module | Contents |
| --- | --- |
| [Definitions](GaupenovGuyonVenier/Definitions.lean) | Integer witness, canonical transition, and conjecture statement |
| [Preservation](GaupenovGuyonVenier/Preservation.lean) | Persistence of the initial state |
| [Stability](GaupenovGuyonVenier/Stability.lean) | Exclusion of strict descent |
| [Main theorem](GaupenovGuyonVenier/Proof.lean) | Announced counterexample and negation of the conjecture |
| [Reference certificate](GaupenovGuyonVenier/Certificate.lean) | Base-256 representation and supplementary reference |
| [Textual certificates](GaupenovGuyonVenier/TextCertificates.lean) | Exact reconstruction of the two auxiliary coefficients |

## Verification

With [Lean and Lake installed](https://lean-lang.org/install/), run:

```sh
lake build
lake exe ggv
python3 scripts/verify_certificate.py
```

The toolchain is pinned in `lean-toolchain`. The project uses Lean core only;
there are no external package dependencies.

The disproof, announced counterexample, and textual certificates have been
checked with Lean 4.19.0. There are no `sorry` placeholders or user-added
axioms. The refutation uses Lean's standard `propext` axiom through integer
order; the textual certificates have empty axiom reports. The Python
reproducer separately checks the SHA-256 provenance of the announced integer.

## License

Original code and documentation are available under the [MIT license](LICENSE).
Third-party material and external references retain their respective rights.
