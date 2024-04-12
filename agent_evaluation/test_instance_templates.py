from abc import ABC, abstractmethod
from rouge_score import rouge_scorer


CHAIN_OF_THOUGHT = ' Think step by step. First, reason about the question and write a short explanation of your answer. Then, on a separate line, write "Final answer:" followed by your final answer to the question.'

class TestInstance(ABC):
    @abstractmethod
    def question(self) -> str:
        return ""
    
    @abstractmethod
    def check_answer(self, answer: str) -> float:
        """Returns a value between 0 and 1 indicating the correctness of the answer."""
        return 0
    
    def extract_answer(self, llm_answer: str) -> str:
        _, _, final_answer = llm_answer.partition("Final answer:")
        final_answer = final_answer.lstrip("*")  # remove bold text from "**Final answer:** no"
        return final_answer


class YesNoQuestion(TestInstance):
    """Question with response "yes" or "no"."""

    def __init__(self, question: str, is_true: bool):
        self._question = question
        self._correct_answer = "yes" if is_true else "no"

    def question(self) -> str:
        # return self._question + ' Respond with either "yes" or "no" and nothing else.'
        return self._question + CHAIN_OF_THOUGHT + ' Your final answer must be either "yes" or "no".'

    def check_answer(self, answer: str) -> float:
        answer = self.extract_answer(answer)
        answer = answer.strip().strip('".').lower()

        if answer == self._correct_answer:
            return 1
        else:
            return 0


class SetQuestion(TestInstance):
    """Response to this question is a set of values."""

    def __init__(self, question: str, correct_answer: set[str]):
        self._question = question
        self._correct_answer = correct_answer

    def question(self) -> str:
        return self._question + CHAIN_OF_THOUGHT + ' Your final answer must be a comma separated list of values.'

    def check_answer(self, answer: str) -> float:
        answer = self.extract_answer(answer)
        answers = set(answer.replace(" ", "").split(","))

        if len(self._correct_answer) == 0:
            if answer.strip().lower() in ("", "none"):
                return 1
            return 0

        # compute Jaccard similarity (size of intersection / size of union)
        intersection = answers.intersection(self._correct_answer)
        union = answers.union(self._correct_answer)
        jaccard_similarity = len(intersection) / len(union)

        return jaccard_similarity
    

class OpenQuestion(TestInstance):
    """Response to this question is a string."""

    def __init__(self, question: str, reference_answer: str):
        self._question = question
        self._reference_answer = reference_answer

    def question(self) -> str:
        return self._question #+ CHAIN_OF_THOUGHT

    def check_answer(self, answer: str) -> float:
        # answer = self.extract_answer(answer)

        scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=False)
        scores = scorer.score(self._reference_answer, answer)['rouge1']

        return scores.recall


def instance_generator(category: str, test_instances_for_category: dict[str, list[TestInstance]]):
    for pattern, test_instances in test_instances_for_category.items():
            for test_instance in test_instances:
                yield category, pattern, test_instance
