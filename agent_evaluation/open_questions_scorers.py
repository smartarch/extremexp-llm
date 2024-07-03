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
        score = self._scorer.score(reference, candidate)['rouge1']
        # print(score.precision, score.recall, score.fmeasure)

        return score.fmeasure
    

class BertScorer(Scorer):

    def __init__(self):
        self._scorer = BERTScorer(lang="en", rescale_with_baseline=True)

    def score(self, reference: str, candidate: str) -> float:
        precision, recall, f1 = self._scorer.score([reference], [candidate])
        # print(precision, recall, f1)

        return float(f1[0])
