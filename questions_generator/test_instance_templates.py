from abc import ABC, abstractmethod

class TestInstance(ABC):
    @abstractmethod
    def question(self) -> str:
        return ""
    
    @abstractmethod
    def check_answer(self, answer: str) -> float:
        """Returns a value between 0 and 1 indicating the correctness of the answer."""
        return 0


class YesNoQuestion(TestInstance):

    def __init__(self, question: str, is_true: bool):
        self._question = question
        self._correct_answer = "yes" if is_true else "no"

    def question(self) -> str:
        # return self._question + ' Respond with either "yes" or "no" and nothing else.'
        return self._question + ' On the first line of your response, write either "yes" or "no" and nothing else. On the second, write a short justification of the answer.'

    def check_answer(self, answer: str) -> float:
        answer, _, _ = answer.partition("\n")
        answer = answer.strip().strip('".').lower()

        if answer == self._correct_answer:
            return 1
        else:
            return 0
