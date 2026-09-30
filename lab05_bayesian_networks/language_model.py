"""First- and second-order count-based language models; no ML library needed."""
from collections import Counter, defaultdict
from itertools import product
import random

START, END = '<START>', '<END>'
SENTENCES = ['the cat sat on the mat', 'the cat sat on the rug',
             'the dog sat on the mat', 'the dog ran to the park',
             'the cat ran to the park', 'the dog sat on the rug']


class LanguageModel:
    def __init__(self, sentences, order=1):
        if order not in (1, 2):
            raise ValueError('Order must be 1 or 2')
        self.order = order
        self.counts = defaultdict(Counter)
        self.vocabulary = {END}
        for sentence in sentences:
            words = sentence.lower().split() if isinstance(sentence, str) else [w.lower() for w in sentence]
            self.vocabulary.update(words)
            tokens = [START] * order + words + [END]
            for i in range(order, len(tokens)):
                self.counts[tuple(tokens[i-order:i])][tokens[i]] += 1
        self.probabilities = {context: {word: n / sum(counts.values()) for word, n in counts.items()}
                              for context, counts in self.counts.items()}

    def distribution(self, context):
        context = (context,) if isinstance(context, str) else tuple(context)
        if len(context) != self.order:
            raise ValueError('Wrong context length')
        if context not in self.probabilities:
            raise ValueError('Unseen context: ' + repr(context))
        return self.probabilities[context]

    def predict(self, context):
        distribution = self.distribution(context)
        return min(distribution, key=lambda word: (-distribution[word], word))

    def generate(self, mode='sampling', rng=None, max_tokens=50):
        if mode not in ('sampling', 'greedy'):
            raise ValueError('Use sampling or greedy')
        rng = rng or random.Random()
        context, words = (START,) * self.order, []
        for _ in range(max_tokens):
            distribution = self.distribution(context)
            nxt = (self.predict(context) if mode == 'greedy' else
                   rng.choices(list(distribution), weights=list(distribution.values()), k=1)[0])
            if nxt == END:
                return {'text': ' '.join(words), 'terminated': True}
            words.append(nxt)
            context = (*context[1:], nxt)
        return {'text': ' '.join(words), 'terminated': False}

    def statistics(self):
        # Candidate previous tokens: START plus ordinary words, excluding terminal END.
        previous = sorted((self.vocabulary - {END}) | {START})
        contexts = list(product(previous, repeat=self.order))
        entries = sum(len(row) for row in self.probabilities.values())
        return {'observed_contexts': len(self.probabilities), 'candidate_contexts': len(contexts),
                'unseen_contexts': sum(c not in self.probabilities for c in contexts),
                'nonzero_cpt_entries': entries,
                'free_parameters_observed_rows': entries - len(self.probabilities),
                'dense_cpt_entries': len(contexts) * len(self.vocabulary),
                'zero_entries_in_observed_rows': len(self.probabilities) * len(self.vocabulary) - entries}


if __name__ == '__main__':
    for order in (1, 2):
        print('\nOrder:', order)
        model = LanguageModel(SENTENCES, order)
        contexts = ([(w,) for w in ['the', 'cat', 'dog', 'sat', 'ran']] if order == 1 else
                    [('the', 'cat'), ('the', 'dog'), ('cat', 'sat'), ('sat', 'on'), ('to', 'the')])
        for context in contexts:
            print(context, model.distribution(context), 'prediction:', model.predict(context))
        print('Normalization checks')
        for context, row in model.probabilities.items():
            total = sum(row.values())
            assert abs(total - 1) < 1e-12
            print(context, total)
        rng = random.Random(67)
        sampled = [model.generate(rng=rng) for _ in range(20)]
        print('20 generated sentences')
        for sentence in sampled:
            print(sentence['text'], '' if sentence['terminated'] else '[length limit]')
        print('Five greedy sentences')
        for _ in range(5):
            sentence = model.generate('greedy')
            print(sentence['text'], '' if sentence['terminated'] else '[length limit]')
        print('Five sampled sentences')
        for _ in range(5):
            sentence = model.generate(rng=rng)
            print(sentence['text'], '' if sentence['terminated'] else '[length limit]')
        print('CPT statistics:', model.statistics())
        print('Distinct sentences among 20:', len({s['text'] for s in sampled}))
