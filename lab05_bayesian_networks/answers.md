# BN lab

The six sentences are lowercased and split into words. START marks the beginning and END marks the end. The first-order model uses one previous word; second order uses two, with two START tokens at the beginning. Both models estimate probabilities by counting, with no smoothing.

Questions 1 and 2

1. The chain rule writes the sequence probability as a product of next-word conditional probabilities. This lets us generate the text one word at a time instead of choosing a whole sentence at once. Each generated word is added to the context for the next prediction.

2. The first-order assumption is P(Xt | X1,...,Xt-1) = P(Xt | Xt-1). Given the previous word, the model treats the next word as independent of the earlier history. This is a simplifying assumption of this model; real language can depend on much earlier words.

Question 3 and next-word predictions

The required first-order probabilities are:

- After the: cat 1/4, dog 1/4, mat 1/6, rug 1/6, park 1/6. Greedy prediction is cat because the code breaks the cat/dog tie alphabetically.
- After cat: sat 2/3, ran 1/3. Prediction is sat.
- After dog: sat 2/3, ran 1/3. Prediction is sat.
- After sat: on 1. Prediction is on.
- After ran: to 1. Prediction is to.

For example, “the cat” occurs three times out of the 12 transitions leaving “the”, giving 3/12 = 1/4. There are 12 rather than six because “the” appears at sentence starts and before final nouns. Unlisted successors in these rows have probability zero, such as P(dog | cat) and P(cat | sat).

Questions 4 to 9

4. The transition counts are in `self.counts`. Each key is a context tuple and its Counter records how often each next word followed it. First-order keys contain one token; second-order keys contain two.

5. `self.probabilities` is calculated in the constructor. Each successor count is divided by the sum of all successor counts for that context, including END. This gives P(next word | context).

6. `predict` returns the most probable next word. In sampling mode, `generate` uses `rng.choices` with the row probabilities. Greedy selection always picks the same best word under the tie rule, while sampling can also select less probable words.

7. If a context has no observed transitions, `distribution` raises ValueError because this unsmoothed model has no estimated probability row for it. END is handled separately by stopping generation. Smoothing or backoff could handle unseen contexts, but they are not part of this implementation.

8. A row total of 0.87 means some probability mass is missing. The denominator, transition counts or included successors should be checked; a difference that large is not normal floating-point rounding. In the runs, all 11 first-order rows and all 15 observed second-order rows summed to approximately 1.

9. The model's most probable word need not match what a person expects. After “sat on the”, a person might expect mat, but first order sees only “the” and gives cat and dog the highest probabilities. Its prediction reflects the counted data and limited context, rather than a full understanding of the sentence.

Generation and Question 10

The code prints 20 sampled sentences per order and then five greedy and five sampled examples. Seed 67 is used, with the random generator continuing between sentences. Generation stops at END. A 50-word limit prevents an endless sequence if the chosen transitions cycle.

For first order, all five greedy runs cycled through “the cat sat on the” and hit that limit. For second order, all five greedy runs gave “the cat sat on the mat”. Greedy output is repetitive because the same context always leads to the same choice.

The five sampled first-order examples were:

- the cat ran to the mat
- the dog sat on the dog sat on the cat sat on the rug
- the rug
- the cat ran to the dog sat on the park
- the cat sat on the rug

The five sampled second-order examples were:

- the dog sat on the mat
- the cat sat on the mat
- the cat sat on the mat
- the dog sat on the mat
- the cat ran to the park

10. Sampling produced more variation because a context can lead to different successors according to their probabilities. It can still repeat sentences, especially with this small dataset. More variation does not automatically mean more sensible text, as the first-order examples show.

Questions 11 and 12

11. In second order, a word has the previous two words as parents instead of only the previous word. Probability rows are indexed by word pairs and estimated from triples. This gives more context for prediction, but more observations are needed because each pair has its own row.

For example, after “the cat” or “the dog”, sat has probability 2/3 and ran 1/3. After “cat sat”, on has probability 1. After “sat on”, the has probability 1, and after “to the”, park has probability 1.

12. Extra context separates cases that first order combines. “on the” can lead to mat or rug, while “to the” leads to park. This improves coherence, but it spreads a small dataset across many possible contexts, leaving many pairs unseen. The dense table grows roughly from V² entries to V³.

In this dataset, first order has 11 observed contexts, 17 nonzero probability entries and 6 free parameters in the observed rows. Second order has 15 observed contexts, 19 nonzero entries and 4 free parameters in observed rows. A row with k possible observed successors has k-1 free parameters because its probabilities must sum to 1. The smaller observed free-parameter count does not mean the full second-order model needs less data.

Using START plus the ten ordinary words as candidate context tokens gives 11 first-order contexts, all observed. There are 121 candidate second-order pairs, of which 106 are unseen. Some counted pairs, such as a word followed by START, cannot occur in these sentences. With 11 possible output tokens including END, the corresponding dense tables have 121 and 1331 entries. An unseen context has no estimated row; it is different from an observed row with a zero-probability successor.

Among the first 20 samples, first order produced 15 distinct texts and second order produced 6. All 20 reached END for each model. Second order generated the six training-sentence forms in this run, making the text more coherent but less diverse. First order could produce short combinations such as “the rug” or mix phrases in longer sentences.

Questions 13 and 14

13. Approach B is preferable because it states the intended probability model and how it should be estimated. It makes clear that this is transition counting and sampling, not a pretrained model or a neural network. The implementation can then be checked against that model by inspecting counts, denominators and the generation rule. Row sums provide a direct probability check, while sensible-looking text alone would not show that the right model was implemented.

14. The BN view makes the dependency assumptions explicit: first order uses one previous word, and second order uses two. It gives a factorization of the joint probability and explains why repeated conditional sampling generates a sequence. It also helps explain why extra context needs more probability rows, and supplies checks such as every observed conditional distribution summing to 1.

A modern autoregressive language model also predicts P(xt | x1,...,xt-1). It uses learned neural weights and much larger contexts instead of a small count-based table. The next-token conditional probability idea stays the same, but its representation and ability to use context are very different.

The LLM helped implement counting, normalization and generation. One inspected part was the denominator in `self.probabilities`: it must include every successor count, including END. The row totals and generated examples were then checked to see whether the code followed the intended model.
