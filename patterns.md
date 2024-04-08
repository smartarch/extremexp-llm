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

### Conditional flow

Rationale: Can the LLM evaluate conditional flow?

Parameters:

* $F$: flow type (e.g., control flow)
* $W$: workflow name
* $T_0, \dots, T_K$: tasks in the workflow
* $C_1, \dots, C_K$: conditions for conditional links (in flow $F$)
* $S$: situation (e.g., parameter values)

Architecture: Workflow $W$ with tasks $T_0, \dots, T_K$ (and possibly other), conditional links in flow $F$ between $T_0$ and $T_1$, \dots, $T_K$ with conditions $C_1, \dots, C_K$ respectively. Situation $S$ such that $C_1$ is true and $C_2, \dots, C_K$ are false.

Question: Which task will follow $T_0$ in flow $F$ in workflow $W$?

Reference answer: $T_1$

Evaluation metric: correctness ($1$ if LLM's answer is correct, $0$ otherwise)

Example instance: "Which task will follow `HyperparameterProposal' in control flow in workflow `HyperparameterOptimization'?"

## Semantics patterns

TODO

### Inconsistent descriptions

Rationale: Can the LLM detect inconsistent descriptions of workflow and tasks?

Parameters:

* $W$: workflow name
* $D_W$: workflow description
* $D_T$: task description that is inconsistent with $D_W$

Architecture: Workflow containing a task with inconsistent description.

Question: Identify potential errors in the specification of $W$ and present a list of them.

Reference answer: *description of the inconsistency (depends on the test instance)*

Evaluation metric: ROUGE

Example instance: A workflow specifying an ML pipeline where the ML goal is said to be "binary classification" in the workflow description. At the same time, the tasks perform training of a "regression" ML model (which is inconsistent with "binary classification").

### Semantically incorrect order of tasks

Rationale: Can the LLM detect tasks that are clearly in wrong order (semantically)?

Parameters:

* $W$: workflow name
* $T_1, T_2$: tasks in $W$
* $F$: flow type (e.g., control flow)

Architecture: Workflow $W$ containing tasks $T_1, T_2$ (and possibly other). In flow $F$, the link $T_1 \to T_2$ is semantically incorrect.

Question: Identify potential errors in the specification of $W$ and present a list of them.

Reference answer: Task $T_2$ should preceed task $T_1$ in flow $F$. *(concrete formulation depends on the test instance)*

Evaluation metric: ROUGE

Example instance: Workflow with task 'MLModelTraining' after 'MLModelEvaluation'.

## Evaluation metrics used in the patterns

### Yes-no questions, questions with one correct answer

* **correctness**: $1$ if LLM's answer = reference answer, $0$ otherwise

### Set questions

* **Jaccard index**: the size of the intersection divided by the size of the union of the sets (LLM's answer set and the reference answer set)

### Open questions (semantics)

* [**ROUGE**](https://aclanthology.org/W04-1013/) (Recall-Oriented Understudy for Gisting Evaluation): the word overlap of the reference answer and the LLM output
* [**BERTScore**](https://arxiv.org/abs/1904.09675): the cosine similarity of word embeddings (that capture the meaning of words)
* **manual**: manual assessment of the LLM's output
* **LLM as a judge** (e.g., [G-Eval](https://arxiv.org/abs/2303.16634)): use another LLM to assess the LLM's output
