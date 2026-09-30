# Bayesian networks

The six sentences are lowercased and split into words. The first-order model uses one START token and the second-order model uses two. Both use END. Probabilities come from transition counts, without smoothing.

## Probability results

First-order distributions and greedy predictions:

- the: cat 1/4, dog 1/4, mat 1/6, rug 1/6, park 1/6. Prediction: cat (tie broken alphabetically).
- cat: sat 2/3, ran 1/3. Prediction: sat.
- dog: sat 2/3, ran 1/3. Prediction: sat.
- sat: on 1. Prediction: on.
- ran: to 1. Prediction: to.

Other successors have probability zero in these rows. For example, P(dog | cat) = 0.

Second-order examples: after “the cat” or “the dog”, sat has probability 2/3 and ran 1/3. After “cat sat”, on has probability 1. After “sat on”, the has probability 1. After “to the”, park has probability 1.

All 11 first-order and 15 second-order observed probability rows summed to 1. The code prints the totals.

## Generation and comparison

The program prints 20 sampled sentences for each model, then five greedy and five sampled examples. It uses seed 67 and stops at END, with a 50-word safety limit.

First-order greedy generation cycles through “the cat sat on the” and reaches the limit. Second-order greedy generation gives “the cat sat on the mat” every time.

Sampled first-order examples included “the cat ran to the mat”, “the rug” and “the cat sat on the rug”. Second-order examples included “the dog sat on the mat”, “the cat sat on the mat” and “the cat ran to the park”.

First order had 17 nonzero probabilities and 6 free parameters. Second order had 19 nonzero probabilities and 4 free parameters in observed rows. A row with k successors has k−1 free parameters.

Using START and the ten ordinary words as possible context tokens, first order has 11 candidate contexts with none unseen. Second order has 121 candidate pairs, with 106 unseen. Some of those pairs are impossible in a sentence, such as a word followed by START. Dense tables would have 121 and 1331 entries respectively.

Among 20 samples, first order gave 15 distinct texts and second order gave 6. All 20 reached END for both models. Second order was more coherent in this run, but less varied.

## Questions 1–14

1. The chain rule lets us generate one word at a time using a conditional probability for the next word.
2. First order assumes P(Xt | X1,...,Xt−1) = P(Xt | Xt−1). Earlier words are independent of Xt once Xt−1 is known.
3. The required distributions are listed above. The word “the” has 12 outgoing occurrences because it appears at the start and before final nouns.
4. Transition counts are in `self.counts`, mapping context tuples to Counters.
5. `probabilities` divides each next-word count by the context's total count.
6. `predict` picks the most probable word. Sampling uses `rng.choices` with the probabilities, so less likely words can also appear.
7. An unseen context raises ValueError. END stops generation before another prediction is requested.
8. A total of 0.87 means probabilities are missing or normalization is wrong.
9. No. After “the”, cat and dog tie, even when a person expects mat after “sat on the”. First order has forgotten those earlier words.
10. Sampling gives more variation because it can choose different successors. Greedy generation always follows the same tie rule.
11. Second order gives each word two previous parents, uses pair-indexed probability rows and keeps two words of context. More data is needed to estimate those rows.
12. More context distinguishes phrases, but splits observations across more contexts. Dense table size grows from roughly V² to V³, making estimates sparse.
13. Approach B states the model, representation and required behaviour clearly. Counts, normalization and sampling can then be checked against that specification.
14. The BN view shows dependencies, independence assumptions and joint factorization. It also gives a generation method and checks such as probability rows summing to one.

## Reflection

The full chain rule uses P(xt | x1,...,xt−1). These models approximate that history with one or two words. Modern neural language models use learned weights and larger contexts, while still predicting the next token conditionally.

The LLM helped implement the counting and generation code. The normalization calculation was inspected to check that all outgoing transitions, including END, were included in the denominator. Row sums and generated examples were then checked.
