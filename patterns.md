# Test instance patterns

This is a full list of test instance *patterns* that can be used for evaluating understanding workflow architectures by LLMs.

To create *test instances* from the patterns, substitute all the parameters.

## Structure patterns

### List of tasks

Rationale: Can the LLM list the tasks in a workflow and filter them?

Parameters:

* $P$: property of the tasks (e.g., the task has a parameter), can be empty (to list all the tasks)
* $N$: number of tasks satisfying $P$
* $T$: total number of tasks
* $W$: workflow name

Architecture: Workflow $W$ with $N$ tasks satisfying $P$ and $T-N$ tasks not satisfying $P$.

Question: List all tasks in workflow $W$ that satisfy $P$.

Reference answer: *a set of $N$ tasks satisfying $P$ (depends on the parameter substitution for the test instance)*

Evaluation metric: Jaccard index

Example instance: "List all tasks in workflow 'MLTrainingAndEvaluation' that have a parameter."

### Flow cycle

Rationale: Can the LLM find cycles in the flow?

Parameters:

* $F$: flow type (e.g., control flow, data flow)
* $C$: length of the cycle
* $W$: workflow name

Architecture: Workflow $W$ with a cycle of length $C$ among the tasks (circular flow $F$ among several tasks).

Question: In workflow $W$, is there a cycle in the $F$?

Reference answer: yes

Evaluation metric: correctness

---

Rationale: Can the LLM find cycles in the flow? (negative test)

Parameters:

* $F$: flow type (e.g., control flow, data flow)
* $W$: workflow name

Architecture: Workflow $W$ without a cycle in flow $F$ among the tasks.

Question: In workflow $W$, is there a cycle in the $F$?

Reference answer: no

Evaluation metric: correctness

### Recursive sub-workflows

TODO

### Dependency (in the flow)

Rationale: Can the LLM understand dependencies (in the flow)?

Parameters:

* $W$: workflow name
* $E$: entity (e.g., task, data) in the workflow
* $T$: task in the workflow that depends on $E$ (trough e.g., control flow, data flow)

Architecture: Workflow $W$ with task $T$ that depends on $E$.

Question: In workflow $W$, does $T$ depend on $E$?

Reference answer: yes

Evaluation metric: correctness

Example instances:

* "In workflow 'MLTrainingAndEvaluation' does task 'MLModelEvaluation' depend on task 'MLModelTraining'?"
* "In workflow 'MLTrainingAndEvaluation' does task 'MLModelTraining' depend on data 'TrainingData'?"

---

Rationale: Can the LLM understand dependencies (in the flow)? (negative test)

Parameters:

* $W$: workflow name
* $E$: entity (e.g., task, data) in the workflow
* $T$: task in the workflow that does not depend on $E$ (trough e.g., control flow, data flow)

Architecture: Workflow $W$ with task $T$ that does not depend on $E$.

Question: In workflow $W$, does $T$ depend on $E$?

Reference answer: not

Evaluation metric: correctness

Example instances:

* "In workflow 'MLTrainingAndEvaluation' does task 'MLModelTraining' depend on task 'MLModelEvaluation'?"
* "In workflow 'MLTrainingAndEvaluation' does task 'MLModelTraining' depend on data 'TestData'?"

## Behavior patterns

TODO

## Semantics patterns

TODO

## Evaluation metrics used in the patterns

### Yes-no questions

* **correctness**: $1$ if LLM's answer = reference answer, $0$ otherwise

### Set questions

* **Jaccard index**: the size of the intersection divided by the size of the union of the sets (LLM's answer set and the reference answer set)

### Open questions (semantics)

* [**ROUGE**](https://aclanthology.org/W04-1013/) (Recall-Oriented Understudy for Gisting Evaluation): the word overlap of the reference answer and the LLM output
* [**BERTScore**](https://arxiv.org/abs/1904.09675): the cosine similarity of word embeddings (that capture the meaning of words)
* **manual**: manual assessment of the LLM's output
* **LLM as a judge** (e.g., [G-Eval](https://arxiv.org/abs/2303.16634)): use another LLM to assess the LLM's output
