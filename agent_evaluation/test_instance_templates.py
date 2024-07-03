from abc import ABC, abstractmethod
from collections import defaultdict

from open_questions_scorers import BertScorer, RougeScorer, Scorer


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

    def __init__(self, question: str, reference_answer: str, scorer:Scorer=BertScorer()):
        self._question = question
        self._reference_answer = reference_answer
        self._scorer = scorer

    def question(self) -> str:
        return self._question #+ CHAIN_OF_THOUGHT

    def check_answer(self, answer: str) -> float:
        # answer = self.extract_answer(answer)
        return self._scorer.score(self._reference_answer, answer)


def instance_generator(category: str, test_instances_for_category: dict[str, list[TestInstance]]):
    for pattern, test_instances in test_instances_for_category.items():
            for test_instance in test_instances:
                yield category, pattern, test_instance


class TaskListOpenQuestion(OpenQuestion):
    """Response to this question is a list of tasks, each with a string including more details."""

    def __init__(self, question: str, reference_answer: dict[str, str], scorer:Scorer=BertScorer()):
        self._question = question
        self._reference_answer = reference_answer
        self._scorer = scorer

    def question(self) -> str:
        return self._question + CHAIN_OF_THOUGHT + ' Your final answer must be a list of tasks. Write one task per line. Each line must start with the name of the task, followed by a colon (":"), and then one sentence describing why the task is included.'
    
    def check_answer(self, answer: str) -> float:
        answer = self.extract_answer(answer)
        scores = defaultdict(float)

        for task_row in answer.split("\n"):
            task_tokens = task_row.split(" ")
            if len(task_tokens) == 0 or all(map(lambda t: t == "", task_tokens)):
                continue
            
            if task_tokens[0] == "-" or (task_tokens[0] and task_tokens[0][0].isdigit()):  # correctly parse bullets ("-") and numbered lists
                task_name = task_tokens[1]
            else:
                task_name = task_tokens[0]
            task_name = task_name.rstrip(": ")
            if "." in task_name:  # remove names of parent tasks for nested tasks
                task_name = task_name.rsplit(".", 1)[-1]

            _, _, explanation = task_row.partition(":")
            explanation = explanation.lstrip()

            if task_name in self._reference_answer:
                score = self._scorer.score(self._reference_answer[task_name], explanation)
                scores[task_name] = score
                print(f"  {task_name}: {score:.3f}")

        return sum(scores[reference_task] for reference_task in self._reference_answer) / len(self._reference_answer)
