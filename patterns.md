# Test instance patterns

This is a full list of test instance *patterns* that can be used for evaluating understanding workflow architectures by LLMs.

To create *test instances* from the patterns, substitute all the parameters. Note that it might also be necessary to alter the question formulations to adapt them to the language of the specific workflow architecture.

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

---

### Task links in flow

Rationale: Can the LLM understand flow links between tasks?

Parameters:

* $F$: flow type (e.g., control flow, data flow)
* $W$: workflow name
* $T_1, T_2$: tasks in $W$

Architecture: Workflow $W$ with tasks $T_1, T_2$ (and possibly other), linked $T_1 \to T_2$ in flow $F$.

Question: In workflow $W$, does $T_2$ directly follow $T_1$ in flow $F$?

Reference answer: yes

Evaluation metric: correctness

Example instance: "In workflow 'MLTrainingAndEvaluation', does 'MLModelEvaluation' directly follow 'MLModelTraining' in control flow?"

---

Rationale: Can the LLM understand flow links between tasks? (negative test)

Parameters:

* $F$: flow type (e.g., control flow, data flow)
* $W$: workflow name
* $T_1, T_2$: tasks in $W$

Architecture: Workflow $W$ with tasks $T_1, T_2$ (and possibly other). There is no link $T_1 \to T_2$ in flow $F$.

Question: In workflow $W$, does $T_2$ directly follow $T_1$ in flow $F$?

Reference answer: no

Evaluation metric: correctness

Example instance: "In workflow 'MLTrainingAndEvaluation', does 'MLModelTraining' directly follow 'MLModelEvaluation' in control flow?"

---

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

---

### Task hierarchy (if the architecture is hierarchical)

Rationale: Can the LLM understand task hierarchy (if the architecture is hierarchical)?

Parameters:

* $W$: workflow name
* $T$: task in the workflow $W$ that is composite (has sub-tasks)
* $S$: sub-task of $T$

Architecture: Workflow $W$ with task $T$ that has sub-tasks (sub-workflow). One of the sub-tasks is $S$.

Question: Is task $S$ a part of task $T$ (from workflow $W$)?

Reference answer: yes

Evaluation metric: correctness

Example instance: "Is task 'HyperparameterProposal' a part of task 'HyperparameterOptimization' (from workflow 'FailurePredictionInManufacture')?"

---

Rationale: Can the LLM understand task hierarchy (if the architecture is hierarchical)? (negative test)

Parameters:

* $W$: workflow name
* $T$: task in the workflow $W$ (it might be composite)
* $S$: a different task from $W$ (or another workflow) that is not sub-task of $T$

Architecture: Workflow $W$ with task $T$. Another task $S$, that is not sub-task of $T$.

Question: Is task $S$ a part of task $T$ (from workflow $W$)?

Reference answer: no

Evaluation metric: correctness

Example instance: "Is task 'DataRetrieval' a part of task 'HyperparameterOptimization' (from workflow 'FailurePredictionInManufacture')?"

---

### Infinite recursion in references

Rationale: Can the LLM detect infinite recursion in references (e.g., sub-workflows if the architecture is hierarchical)?

Parameters:

* $W$: workflow name

Architecture: Workflow $W$ that references itself in the workflow.

Question: In workflow $W$, is there an infinite recursion in the references?

Reference answer: yes

Evaluation metric: correctness

Note: The recursion might also be more complicated than just a simple self-reference, i.e., $W_1$ references $W_2$, $W_2$ references $W_3$, $\dots$, $W_K$ references $W_1$.

---

Rationale: Can the LLM detect infinite recursion in references (e.g., sub-workflows if the architecture is hierarchical)? (negative test)

Parameters:

* $W$: workflow name

Architecture: Workflow $W$ without infinite recursion of references.

Question: In workflow $W$, is there an infinite recursion in the references?

Reference answer: no

Evaluation metric: correctness

---

### Dependency (in the flow)

Rationale: Can the LLM understand dependencies (in the flow)?

Parameters:

* $W$: workflow name
* $E$: entity (e.g., task, data) in the workflow
* $T$: task in the workflow that depends on $E$ (trough e.g., control flow, data flow)

Architecture: Workflow $W$ with task $T$ that depends on $E$ (the dependency might be transitive through other entities).

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

Reference answer: no

Evaluation metric: correctness

Example instances:

* "In workflow 'MLTrainingAndEvaluation' does task 'MLModelTraining' depend on task 'MLModelEvaluation'?"
* "In workflow 'MLTrainingAndEvaluation' does task 'MLModelTraining' depend on data 'TestData'?"

---

### List of dependencies (in the flow)

Rationale: Can the LLM list dependencies (in the flow)?

Parameters:

* $W$: workflow name
* $E$: entity type (e.g., task, data)
* $E_1, \dots, E_K$: entities (of type $E$) in the workflow
* $T$: task in the workflow that depends on $E_1, \dots, E_K$

Architecture: Workflow $W$ with task $T$ that depends on $E_1, \dots, E_K$.

Question: List all *entities of type $E$* that $T$ (from $W$) depends.

Reference answer: $\{E_1, \dots, E_K\}$

Evaluation metric: Jaccard index

Example instances:

* "List all data that task 'MLModelEvaluation' (from workflow 'MLTrainingAndEvaluation') depends on.", reference answer: { MLModel, TestFeatures }
* "List all tasks that must run before task 'MLModelEvaluation' in workflow 'MLTrainingAndEvaluation'.", reference answer: { FeatureExtraction, ModelTraining }

---

### Data production

Rationale: Can the LLM detect which task produces the given data?

Parameters:

* $W$: workflow name
* $D$: data (or other entity) in the workflow
* $T$: task which produces $D$ as its output

Architecture: Workflow $W$ with task $T$ that produces $D$.

Question: In workflow $W$, which task produces $D$?

Reference answer: $T$

Evaluation metric: correctness

Example instance: "In workflow 'MLTrainingAndEvaluation' which task produces 'MLModel'?", reference answer: 'MLModelTraining'

---

## Behavior patterns

### Trace of tasks

Rationale: Can the LLM determine if a trace of tasks can occur?

Parameters:

* $W$: workflow name
* $T_1, \dots, T_K$: tasks in the workflow $W$
* $S$: situation (e.g., parameter values)
* $R_1, \dots, R_L$ ($L \le K$): tasks that will run when the workflow is executed with initial situation $S$

Architecture: Workflow $W$ with tasks $T_1, \dots, T_K$. When $W$ is executed with initial situation $S$, tasks $R_1, \dots, R_L$ will run in this order.

Question: Can the trace of tasks $R_1, \dots, R_K$ occur in workflow $W$ in this order?

Reference answer: yes

Evaluation metric: correctness

Example instance: "Can the trace of tasks 'FeatureExtraction', 'MLModelTraining', 'MLModelEvaluation' occur in workflow 'MLTrainingAndEvaluation'?"

---

Rationale: Can the LLM determine if a trace of tasks can occur? (negative test)

Parameters:

* $W$: workflow name
* $T_1, \dots, T_K$: tasks in the workflow $W$
* $R_1, \dots, R_L$: tasks (from $W$ or different workflow)

Architecture: Workflow $W$ with tasks $T_1, \dots, T_K$. When $W$ is executed (with any initial situation), the tasks that will run will not be exactly $R_1, \dots, R_L$ in this order.

Question: Can the trace of tasks $R_1, \dots, R_K$ occur in workflow $W$ in this order?

Reference answer: no

Evaluation metric: correctness

Example instance: "Can the trace of tasks 'TrainTestSplit', 'MLModelEvaluation', 'MLModelTraining' occur in workflow 'MLTrainingAndEvaluation'?"

---

### Task order (without conditional flow)

Rationale: Can the LLM understand the order of tasks in the workflow without conditional flow?

Parameters:

* $W$: workflow name
* $T_1, \dots, T_K$: tasks in the workflow $W$

Architecture: Workflow $W$ with tasks $T_1, \dots, T_K$ in this order in control flow.

Question: List all the tasks in workflow $W$ in order in which they run.

Reference answer: $T_1, \dots, T_K$ *(note: if some tasks can run in parallel, they can be listed in any order)*

Evaluation metric: Damerau–Levenshtein distance *(note: special care must be given to the order of parallel tasks)*

Example instance: "List all the tasks in workflow 'MLTrainingAndEvaluation' in order in which they run.", reference answer: FeatureExtraction, MLModelTraining, MLModelEvaluation

---

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

Example instance: "Which task will follow 'HyperparameterProposal' in control flow in workflow 'HyperparameterOptimization'?"

---

### Task order (with conditional flow)

Rationale: Can the LLM understand the order of tasks in the workflow with conditional flow?

Parameters:

* $W$: workflow name
* $T_1, \dots, T_K$: tasks in the workflow $W$
* $S$: situation (e.g., parameter values)
* $R_1, \dots, R_L$ ($L \le K$): tasks that will run when the workflow is executed with initial situation $S$

Architecture: Workflow $W$ with tasks $T_1, \dots, T_K$. When $W$ is executed with initial situation $S$, tasks $R_1, \dots, R_L$ will run in this order.

Question: Given the initial situation $S$, list all the tasks that will run when workflow $W$ is executed in order in which they will run.

Reference answer: $R_1, \dots, R_L$ *(note: if some tasks can run in parallel, they can be listed in any order)*

Evaluation metric: Damerau–Levenshtein distance *(note: special care must be given to the order of parallel tasks)*

Example instance: "Given the initial situation p=0, list all the tasks that will run when workflow 'Workflow3' is executed in order in which they will run.", reference answer: Task7, Task8

---

## Semantics patterns

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

---

### Semantically incorrect order of tasks

Rationale: Can the LLM detect tasks that are clearly in wrong order (semantically)?

Parameters:

* $W$: workflow name
* $T_1, T_2$: tasks in $W$
* $F$: flow type (e.g., control flow)

Architecture: Workflow $W$ containing tasks $T_1, T_2$ (and possibly other). In flow $F$, the link $T_1 \to T_2$ is semantically incorrect.

Question: Identify potential errors in the specification of $W$ and present a list of them.

Reference answer: Task $T_2$ should precede task $T_1$ in flow $F$. *(concrete formulation depends on the test instance)*

Evaluation metric: ROUGE

Example instance: Workflow with task 'MLModelTraining' after 'MLModelEvaluation'.

---

### Understanding properties (meaning) of tasks

Rationale: Can the LLM understand meaning of tasks (e.g., task performs an operation that is not directly mentioned in the name)?

Parameters:

* $W$: workflow name
* $P$: property of task (e.g., the task is part of data preprocessing)
* $T_1$: task in $W$ with property $P$
* $T_2$: task in $W$

Architecture: Workflow $W$ containing tasks $T_1, T_2$ (and possibly other). Property $P$ is mentioned in description/specification of $T_1$. Task $T_1$ precedes (not necessarily directly) task $T_2$ in the control flow.

Question: Does a task with property $P$ run before $T_2$?

Reference answer: yes

Evaluation metric: correctness

Example instance: Task 'FeatureExtraction' is labeled as "data preprocessing" and it precedes 'MLModelTraining', question: "Does a data preprocessing task run before 'MLModelTraining?"

Note: Other variants of this pattern can also be created, e.g., "Does a task with property $P$ run *after* $T_2$?" (if the order of tasks is appropriately changed in the architecture).

---

Rationale: Can the LLM understand meaning of tasks (e.g., task performs an operation that is not directly mentioned in the name)? (negative test)

Parameters:

* $W$: workflow name
* $P$: property of task (e.g., the task is part of data preprocessing)
* $T_2$: task in $W$

Architecture: Workflow $W$ containing task $T_2$ (and possibly other). No tasks preceding $T_2$ in the control flow satisfy the property $P$.

Question: Does a task with property $P$ run before $T_2$?

Reference answer: no

Evaluation metric: correctness

Example instance: "Does a data preprocessing task run before 'DataRetrieval?" (some of the later tasks might be labeled as "data preprocessing")

Note: Other variants of this pattern can also be created, e.g., "Does a task with property $P$ run *after* $T_2$?" (if the order of tasks is appropriately changed in the architecture).

---

## Evaluation metrics used in the patterns

### Yes-no questions, questions with one correct answer

* **correctness**: $1$ if LLM's answer = reference answer, $0$ otherwise

### Set questions

* **Jaccard index**: the size of the intersection divided by the size of the union of the sets (LLM's answer set and the reference answer set)

### List (ordered) questions

* **Damerau–Levenshtein distance**: edit distance between two sequences allowing insertions, deletions, substitutions, and transposition (swap) of two adjacent elements

### Open questions (semantics)

* [**ROUGE**](https://aclanthology.org/W04-1013/) (Recall-Oriented Understudy for Gisting Evaluation): the word overlap of the reference answer and the LLM output
* [**BERTScore**](https://arxiv.org/abs/1904.09675): the cosine similarity of word embeddings (that capture the meaning of words)
* **manual**: manual assessment of the LLM's output
* **LLM as a judge** (e.g., [G-Eval](https://arxiv.org/abs/2303.16634)): use another LLM to assess the LLM's output
