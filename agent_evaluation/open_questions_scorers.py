from abc import ABC, abstractmethod

# hide the loading messages for BERTScorer
import logging
import transformers
transformers.tokenization_utils.logger.setLevel(logging.ERROR)
transformers.configuration_utils.logger.setLevel(logging.ERROR)
transformers.modeling_utils.logger.setLevel(logging.ERROR)


from rouge_score import rouge_scorer
from bert_score import BERTScorer

class Scorer(ABC):

    @abstractmethod
    def score(self, reference: str, candidate: str) -> float:
        return 0


class RougeScorer(Scorer):

    def __init__(self):
        self._scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=False)

    def score(self, reference: str, candidate: str) -> float:
        scores = self._scorer.score(reference, candidate)['rouge1']

        return scores.recall
    

class BertScorer(Scorer):

    def __init__(self):
        self._scorer = BERTScorer(lang="en", rescale_with_baseline=True)

    def score(self, reference: str, candidate: str) -> float:
        _, recall, _ = self._scorer.score([reference], [candidate])

        return float(recall[0])
