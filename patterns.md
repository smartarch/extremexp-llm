# Test instance patterns

This is a full list of test instance *patterns* that can be used for evaluating understanding workflow architectures by LLMs.

To create *test instances* from the patterns, substitute all the parameters. Note that it might also be necessary to alter the question formulations to adapt them to the language of the specific workflow architecture.

## Overview

### Structure

#### Tasks

* [List of tasks](#list-of-tasks) (in workflow)
* [List of tasks with a property](#list-of-tasks-with-a-property)

#### Flow Links (e.g., control flow)

* [Link existence](#link-existence), [Task after task](#task-after-task)
* [Next tasks in flow](#next-tasks-in-flow)
* [Flow cycle](#flow-cycle)
* [Flow start detection](#flow-start-detection)
* [Flow end detection](#flow-end-detection)
* [Missing link](#missing-link)

Special types of links (e.g., conditional, exceptional):

* [Link existence with a property](#link-existence-with-a-property)
* [List of links with a property](#list-of-links-with-a-property)

Link operators (e.g., parallel flow - fork and join):

* [Operator existence](#operator-existence)
* [Parallel tasks (block) existence](#parallel-tasks-block-existence)
* [List tasks in a parallel (fork-join) block](#list-tasks-in-a-parallel-fork-join-block)
* [Parallel tasks to a specific task](#parallel-tasks-to-a-specific-task)
* [List all parallel tasks](#list-all-parallel-tasks)
* [List tasks in an operator block (other than simple fork-join)](#list-tasks-in-an-operator-block-other-than-simple-fork-join)

#### Dependencies (on other entities, e.g., data)

* [Dependency existence (in the flow)](#dependency-existence-in-the-flow)
* [List of dependencies (in the flow)](#list-of-dependencies-in-the-flow)
* [Data production](#data-production)

#### Hierarchical structure

* [Task hierarchy](#task-hierarchy)
* [List of composite tasks](#list-of-composite-tasks)
* [List of nested tasks](#list-of-nested-tasks)
* [Infinite recursion in references](#infinite-recursion-in-references)

### Behavior

#### Task order

* [Are tasks in correct order? (without conditional flow)](#are-tasks-in-correct-order-without-conditional-flow)
* [Are all tasks in correct order? (without conditional flow)](#are-all-tasks-in-correct-order-without-conditional-flow)
* [Determine task order (without conditional flow)](#determine-task-order-without-conditional-flow)

#### Conditional flow

* [Is conditional flow mutually exclusive?](#is-conditional-flow-mutually-exclusive)
* [Next task in conditional flow](#next-task-in-conditional-flow)
* [Are tasks in correct order? (with conditional flow)](#are-tasks-in-correct-order-with-conditional-flow)
* [Are all tasks in correct order? (with conditional flow)](#are-all-tasks-in-correct-order-with-conditional-flow)
* [Determine task order (with conditional flow)](#determine-task-order-with-conditional-flow)
* [Is loop infinite?](#is-loop-infinite)
* [Loop end condition](#loop-end-condition)

#### Traces

* [Trace of tasks with initial situation](#trace-of-tasks-with-initial-situation)
* [Does task run in every situation?](#does-task-run-in-every-situation)

### Basic functionality

#### Task functionality

* [Describe task functionality](#describe-task-functionality)
* [Inconsistent task name and description](#inconsistent-task-name-and-description)
* [Inconsistent task name and other entities](#inconsistent-task-name-and-other-entities) (e.g., parameters, data)
* [Meaning (functionality) of tasks](#meaning-functionality-of-tasks)

#### Workflow functionality

* [Describe workflow functionality](#describe-workflow-functionality)
* [Inconsistent workflow name and description](#inconsistent-workflow-name-and-description)
* [Inconsistent descriptions of workflow and tasks](#inconsistent-descriptions-of-workflow-and-tasks)

#### Order of tasks

* [Semantically incorrect order of tasks](#semantically-incorrect-order-of-tasks)
* [Meaning (functionality) of preceding tasks](#meaning-functionality-of-preceding-tasks)

## Structure patterns

### List of tasks

Rationale: Can the LLM list the tasks in a workflow?

Parameters:

* $N$: total number of tasks
* $W$: workflow name
* $T_1, \dots, T_N$: tasks in $W$

Architecture: Workflow $W$ with $N$ tasks $T_1, \dots, T_N$.

Question: List all tasks in workflow $W$.

Reference answer: $T_1, \dots, T_N$

Evaluation metric: Jaccard index

Example instance: "List all tasks in workflow 'MLTrainingAndEvaluation'."

---

### List of tasks with a property

Rationale: Can the LLM list the tasks in a workflow and filter them based on a specific property?

Parameters:

* $P$: property of the tasks (e.g., the task has a parameter)
* $N$: number of tasks satisfying $P$
* $T$: total number of tasks
* $W$: workflow name

Architecture: Workflow $W$ with $N$ tasks satisfying $P$ and $T-N$ tasks not satisfying $P$.

Question: List all tasks in workflow $W$ that satisfy $P$.

Reference answer: *a set of $N$ tasks satisfying $P$ (depends on the parameter substitution for the test instance)*

Evaluation metric: Jaccard index

Example instance: "List all tasks in workflow 'MLTrainingAndEvaluation' that have a parameter."

---

### Link existence

Rationale: Can the LLM determine if there is a flow link between two tasks?

Parameters:

* $F$: flow type (e.g., control flow, data flow)
* $W$: workflow name
* $T_1, T_2$: tasks in $W$

Architecture: Workflow $W$ with tasks $T_1, T_2$ (and possibly other), linked $T_1 \to T_2$ in flow $F$.

Question: In workflow $W$, is there a flow $F$ link from $T_2$ to $T_1$?

Reference answer: yes

Evaluation metric: correctness

Example instance: "In workflow 'MLTrainingAndEvaluation', is there a control flow link from 'MLModelTraining' to 'MLModelEvaluation'?"

---

Rationale: Can the LLM determine if there is a flow link between two tasks? (negative test)

Parameters:

* $F$: flow type (e.g., control flow, data flow)
* $W$: workflow name
* $T_1, T_2$: tasks in $W$

Architecture: Workflow $W$ with tasks $T_1, T_2$ (and possibly other). There is no link $T_1 \to T_2$ in flow $F$.

Question: In workflow $W$, is there a flow $F$ link from $T_2$ to $T_1$?

Reference answer: no

Evaluation metric: correctness

Example instance: "In workflow 'MLTrainingAndEvaluation', is there a control flow link from 'MLModelEvaluation' to 'MLModelTraining'?"

---

### Task after task

Rationale: Can the LLM determine if there is a flow link between two tasks?

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

Rationale: Can the LLM determine if there is a flow link between two tasks? (negative test)

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

### Next tasks in flow

Rationale: Can the LLM determine to which tasks there is a flow link from a given task?

Parameters:

* $F$: flow type (e.g., control flow, data flow)
* $W$: workflow name
* $T_0$: task in $W$
* $T_1, \dots, T_N$: tasks in $W$

Architecture: Workflow $W$ with tasks $T_0, \dots, T_N$ (and possibly other). There are links in flow $F$ from task $T_0$ to $T_1, \dots, T_N$.

Question: In workflow $W$, which tasks come directly after $T_0$ in flow $F$?

Alternative question formulation: In workflow $W$, to which tasks there are flow $F$ links from $T_0$?

Reference answer: $T_1, \dots, T_N$

Evaluation metric: Jaccard index

Example instance: "In workflow 'MainWorkflow', which tasks come directly after 'Task2' in the control flow?", reference answer: { "Task1", "Task3" } (block of parallel tasks)

---

### Flow cycle

Rationale: Can the LLM find cycles in a flow?

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

### Flow start detection

Rationale: Can the LLM determine the start of a flow?

Parameters:

* $F$: flow type that has an unique start (e.g., control flow)
* $T$: the first task in flow $F$
* $W$: workflow name

Architecture: Workflow $W$ with some tasks connected by flow $F$. The flow $F$ has a unique start task $T$.

Question: In workflow $W$, which task runs first?

Reference answer: $T$

Evaluation metric: correctness

---

### Flow end detection

Rationale: Can the LLM determine the last task(s) of a flow?

Parameters:

* $F$: flow type (e.g., control flow)
* $W$: workflow name
* $T_1, \dots, T_N$: tasks in $W$ which are last in flow $F$ (can be one task or a list of tasks with no $F$ links from them)

Architecture: Workflow $W$ with some tasks connected by flow $F$. The flow $F$ ends in tasks $T_1, \dots, T_N$ (there are no flow $F$ link from them).

Question: In workflow $W$, which tasks runs last?

Reference answer: $T_1, \dots, T_N$

Evaluation metric: Jaccard index

---

### Missing link

Rationale: Can the LLM detect that a flow is not connected (there is a missing link)?

Parameters:

* $F$: flow type (e.g., control flow)
* $W$: workflow name

Architecture: Workflow $W$ with some tasks connected by flow $F$. The flow $F$ is not connected, i.e., there is no path between start and end of the flow (there is at least one missing link).

Question: In workflow $W$, is the flow $F$ connected?

Reference answer: no

Evaluation metric: correctness

---

Rationale: Can the LLM detect that the flow is not connected (there is a missing link)? (negative test)

Parameters:

* $F$: flow type (e.g., control flow)
* $W$: workflow name

Architecture: Workflow $W$ with some tasks connected by flow $F$. The flow $F$ is correctly connected.

Question: In workflow $W$, is the flow $F$ connected?

Reference answer: yes

Evaluation metric: correctness

---

### Link existence with a property

Rationale: Can the LLM determine whether there is a flow link between two tasks?

Parameters:

* $F$: flow type (e.g., control flow, data flow)
* $P$: property of the links (e.g., it is conditional)
* $W$: workflow name
* $T_1, T_2$: tasks in $W$

Architecture: Workflow $W$ with tasks $T_1, T_2$ (and possibly other), linked $T_1 \to T_2$ in flow $F$ via a link satisfying $P$.

Question: In workflow $W$, is there a flow $F$ link from $T_2$ to $T_1$ satisfying $P$?

Reference answer: yes

Evaluation metric: correctness

Example instance: "In workflow 'HyperparameterOptimization', is there a conditional control flow link from 'HyperparameterProposal' to 'MLModelValidation'?"

---

Rationale: Can the LLM determine if there is a flow link between two tasks? (negative test)

Parameters:

* $F$: flow type (e.g., control flow, data flow)
* $P$: property of the links (e.g., it is conditional)
* $W$: workflow name
* $T_1, T_2$: tasks in $W$

Architecture: Workflow $W$ with tasks $T_1, T_2$ (and possibly other), linked $T_1 \to T_2$ in flow $F$ via a link not satisfying $P$.

Question: In workflow $W$, is there a flow $F$ link from $T_2$ to $T_1$ satisfying $P$?

Reference answer: no

Evaluation metric: correctness

---

### List of links with a property

Rationale: Can the LLM list the links from a given task and filter them based on a specific property?

Parameters:

* $F$: flow type (e.g., control flow, data flow)
* $P$: property of the links (e.g., it is conditional)
* $W$: workflow name
* $T_0$: task in $W$
* $T_1, \dots, T_N, \dots, T_L$: tasks in $W$ ($N < L$)

Architecture: Workflow $W$ with tasks $T_0, \dots, T_L$ (and possibly other). There are links in flow $F$ from task $T_0$ to $T_1, \dots, T_N$ satisfying $P$ and links from $T_0$ to $T_{N+1}, \dots, T_L$ not satisfying $P$.

Question: To which tasks there is a flow $F$ link from $T_0$ satisfying $P$?

Reference answer: $T_1, \dots, T_N$

Evaluation metric: Jaccard index

Example instance: "In workflow 'HyperparameterOptimization', to which tasks are there conditional flow links from 'HyperparameterProposal'?"

Note: It would be possible to also create a pattern to list all links in workflow satisfying a property, however, it is more complicated to evaluate it as we would have to define a format for encoding the links in the answer (encoding tasks is easier).

---

### Operator existence

Rationale: Can the LLM understand operators (e.g., fork, join)? Can it determine whether there is an operator used in a workflow?

*Pattern details to be added.*

### Parallel tasks (block) existence

Rationale: Can the LLM determine whether some tasks can run in parallel?

*Pattern details to be added.*

Reference answer: yes

Evaluation metric: correctness

### List tasks in a parallel (fork-join) block

Rationale: Can the LLM determine which tasks can run in parallel (inside a particular fork-join block)?

*Pattern details to be added.*

Reference answer: list of tasks

### Parallel tasks to a specific task

Rationale: Can the LLM determine which tasks can run in parallel (to a particular task)?

*Pattern details to be added.*

### List all parallel tasks

Rationale: Can the LLM determine which tasks can run in parallel?

*Pattern details to be added.*

Reference answer: several lists of tasks that can be run in parallel (open question)

### List tasks in an operator block (other than simple fork-join)

Rationale: Can the LLM correctly interpret other operators than simple fork-join?

*Pattern details to be added.*

### Dependency existence (in a flow)

Rationale: Can the LLM find dependencies (in a flow)?

Parameters:

* $W$: workflow name
* $E$: entity (e.g., task, data) in the workflow
* $T$: task in the workflow that depends on $E$ (trough e.g., control flow, data flow)

Architecture: Workflow $W$ with task $T$ that depends on $E$ (the dependency might be transitive through other entities). By dependency, we mean there is a path of flow links from $E$ to $T$.

Question: In workflow $W$, does $T$ depend on $E$?

Reference answer: yes

Evaluation metric: correctness

Example instances:

* "In workflow 'MLTrainingAndEvaluation' does task 'MLModelEvaluation' depend on task 'MLModelTraining'?"
* "In workflow 'MLTrainingAndEvaluation' does task 'MLModelTraining' depend on data 'TrainingData'?"

---

Rationale: Can the LLM find dependencies (in a flow)? (negative test)

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

### List of dependencies (in a flow)

Rationale: Can the LLM list dependencies (in a flow)?

Parameters:

* $W$: workflow name
* $E$: entity type (e.g., task, data)
* $E_1, \dots, E_K$: entities (of type $E$) in the workflow
* $T$: task in the workflow that depends on $E_1, \dots, E_K$

Architecture: Workflow $W$ with task $T$ that depends on $E_1, \dots, E_K$.

Question: List all *entities of type $E$* that $T$ (from $W$) depends on.

Reference answer: $\{E_1, \dots, E_K\}$

Evaluation metric: Jaccard index

Example instances:

* "List all data that task 'MLModelEvaluation' (from workflow 'MLTrainingAndEvaluation') depends on.", reference answer: { MLModel, TestFeatures }
* "List all tasks that must run before task 'MLModelEvaluation' in workflow 'MLTrainingAndEvaluation'.", reference answer: { FeatureExtraction, ModelTraining }

---

### Data production

Rationale: Can the LLM detect which task produces specific data?

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

### Task hierarchy

Rationale: Can the LLM interpret task hierarchy well?

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

Rationale: Can the LLM interpret task hierarchy well? (negative test)

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

### List of composite tasks

Rationale: Can the LLM interpret task hierarchy well?

Can be expressed via [List of tasks with a property](#list-of-tasks-with-a-property) by the property that the task is a composite task (has nested sub-tasks).

Example instance: "List all tasks from 'AutoML' workflow that are composite."

---

### List of nested tasks

Rationale: Can the LLM interpret task hierarchy well?

Can be expressed via [List of tasks with a property](#list-of-tasks-with-a-property) by the property that the task is a part of a composite task.

Example instance: "List all tasks that are nested inside composite tasks of 'AutoML' workflow."

---

### Infinite recursion in references

Rationale: Can the LLM detect infinite recursion in references (e.g., among sub-workflows)?

Parameters:

* $W$: workflow name

Architecture: Workflow $W$ that references itself in the workflow.

Question: In workflow $W$, is there an infinite recursion in the references?

Reference answer: yes

Evaluation metric: correctness

Note: The recursion might also be more complicated than just a simple self-reference, i.e., $W_1$ references $W_2$, $W_2$ references $W_3$, $\dots$, $W_K$ references $W_1$.

---

Rationale: Can the LLM detect infinite recursion in references (e.g., among sub-workflows)? (negative test)

Parameters:

* $W$: workflow name

Architecture: Workflow $W$ without infinite recursion of references.

Question: In workflow $W$, is there an infinite recursion in the references?

Reference answer: no

Evaluation metric: correctness

---

## Behavior patterns

### Are tasks in correct order? (without conditional flow)

Rationale: Can the LLM notice that tasks are in incorrect order (not corresponding to the control flow)?

Parameters:

* $W$: workflow name
* $T_0, T_1, \dots, T_N$: tasks in the workflow $W$

Architecture: Workflow $W$ with tasks $T_0, \dots, T_N$. Tasks $T_0$ and $T_1$ are in this order in control flow (not necessarily directly connected by a link, the order might be due to transitivity of many links).

Question: Does task $T_0$ run before $T_1$ in workflow $W$? 

Reference answer: yes

Evaluation metric: correctness

Example instance:
    Architecture: Workflow with control flow: START -> FeatureExtraction -> ModelTraining -> ModelEvaluation -> END
    Question: Does 'FeatureExtraction' run before 'ModelEvaluation'?
    Reference answer: yes

---

Rationale: Can the LLM notice that tasks are in incorrect order (not corresponding to the control flow)? (negative test)

Parameters:

* $W$: workflow name
* $T_0, T_1, \dots, T_N$: tasks in the workflow $W$

Architecture: Workflow $W$ with tasks $T_0, \dots, T_N$. Tasks $T_0$ and $T_1$ are in this order in control flow (not necessarily directly connected by a link, the order might be due to transitivity of many links).

Question: Does task $T_1$ run before $T_0$ in workflow $W$? 

Reference answer: no

Evaluation metric: correctness

Example instance:
    Architecture: Workflow with control flow: START -> FeatureExtraction -> ModelTraining -> ModelEvaluation -> END
    Question: Does 'ModelEvaluation' run before 'FeatureExtraction'?
    Reference answer: no

---

### Are all tasks in correct order? (without conditional flow)

Rationale: Can the LLM notice that tasks are in incorrect order (not corresponding to the control flow)?

Parameters:

* $W$: workflow name
* $T_1, \dots, T_K$: tasks in the workflow $W$

Architecture: Workflow $W$ with tasks $T_1, \dots, T_K$ in this order in control flow. *(note: the order of parallel tasks might not be defined, so the question is about a possible order)*

Question: Can tasks $T_1, \dots, T_K$ run in this order in workflow $W$?

Reference answer: yes

Evaluation metric: correctness

Example instance:
    Architecture: Workflow with control flow: START -> FeatureExtraction -> ModelTraining -> ModelEvaluation -> END
    Question: Can tasks 'FeatureExtraction', 'ModelTraining', 'ModelEvaluation' run in this order?
    Reference answer: yes

---

Rationale: Can the LLM notice that tasks are in incorrect order (not corresponding to the control flow)? (negative test)

Parameters:

* $W$: workflow name
* $T_1, \dots, T_K$: tasks in the workflow $W$

Architecture: Workflow $W$ with tasks $T_1, \dots, T_K$ that are ordered in control flow differently than $T_1, \dots, T_K$. *(note: the order of parallel tasks might not be defined, so the question is about a possible order)*

Question: Can tasks $T_1, \dots, T_K$ run in this order in workflow $W$?

Reference answer: no

Evaluation metric: correctness

Example instance:
    Architecture: Workflow with control flow: START -> FeatureExtraction -> ModelTraining -> ModelEvaluation -> END
    Question: Can tasks 'ModelTraining', 'FeatureExtraction', 'ModelEvaluation' run in this order?
    Reference answer: no

---

### Determine task order (without conditional flow)

Rationale: Can the LLM order the tasks in a workflow without conditional flow to adhere to control flow links?

Parameters:

* $W$: workflow name
* $T_1, \dots, T_K$: tasks in the workflow $W$

Architecture: Workflow $W$ with tasks $T_1, \dots, T_K$ in this order in control flow.

Question: List all the tasks in workflow $W$ in order in which they run.

Reference answer: $T_1, \dots, T_K$ *(note: if some tasks can run in parallel, they can be listed in any order)*

Evaluation metric: Damerau–Levenshtein distance *(note: special care must be given to the order of parallel tasks)*

Example instance: "List all the tasks in workflow 'MLTrainingAndEvaluation' in order in which they run.", reference answer: FeatureExtraction, MLModelTraining, MLModelEvaluation

---

### Is conditional flow mutually exclusive

Rationale: Can the LLM understand conditional flow guards?

Parameters:

* $F$: flow type (e.g., control flow)
* $W$: workflow name
* $T_0, T_1, T_2$: tasks in the workflow
* $C_1, C_2$: conditions for conditional links (in flow $F$) that are mutually exclusive

Architecture: Workflow $W$ with tasks $T_0, T_1, T_2$ (and possibly other), conditional link in flow $F$ between $T_0$ and $T_1$ with condition $C_1$, conditional link in flow $F$ between $T_0$ and $T_2$ with condition $C_2$, $C_1$ and $C_2$ are mutually exclusive

Question: Are conditional links in flow $F$ from task $T_0$ mutually exclusive?

Reference answer: yes

Evaluation metric: correctness ($1$ if LLM's answer is correct, $0$ otherwise)

Example instance: Workflow with a parameter $p$, $C_1$ is "$p < 0$", $C_2$ is "$p \ge 0$".

---

Rationale: Can the LLM understand conditional flow guards? (negative test)

Parameters:

* $F$: flow type (e.g., control flow)
* $W$: workflow name
* $T_0, T_1, T_2$: tasks in the workflow
* $C_1, C_2$: conditions for conditional links (in flow $F$) that are not mutually exclusive

Architecture: Workflow $W$ with tasks $T_0, T_1, T_2$ (and possibly other), conditional link in flow $F$ between $T_0$ and $T_1$ with condition $C_1$, conditional link in flow $F$ between $T_0$ and $T_2$ with condition $C_2$, $C_1$ and $C_2$ are not mutually exclusive

Question: Are conditional links in flow $F$ from task $T_0$ mutually exclusive?

Reference answer: no

Evaluation metric: correctness ($1$ if LLM's answer is correct, $0$ otherwise)

Example instance: Workflow with a parameter $p$, $C_1$ is "$p < 10$", $C_2$ is "$p > 0$" (both conditions can be true simultaneously).

---

### Are tasks in correct order? (with conditional flow)

Rationale: Can the LLM notice that tasks are in incorrect order (not corresponding to the control flow)?

Same as [Are tasks in correct order? (without conditional flow)](#are-tasks-in-correct-order-without-conditional-flow), but some of the control flow links are conditional.

### Are all tasks in correct order? (with conditional flow)

Rationale: Can the LLM notice that tasks are in incorrect order (not corresponding to the control flow)?

Same as [Are all tasks in correct order? (without conditional flow)](#are-all-tasks-in-correct-order-without-conditional-flow), but some of the control flow links are conditional.

### Next task in conditional flow

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

### Determine task order (with conditional flow)

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

### Is loop infinite?

Rationale: Can the LLM determine that a loop is infinite?

*Pattern details to be added.*

### Loop end condition

Rationale: Can the LLM determine under which conditions a loop ends?

*Pattern details to be added.*

### Trace of tasks with initial situation

Rationale: Can the LLM determine that a trace of tasks can occur in a specific initial situation?

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

Rationale: Can the LLM determine that a trace of tasks can occur in a specific initial situation? (negative test)

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

### Does task run in every situation?

Rationale: Can the LLM interpret conditional flow guards correctly?

Parameters:

* $F$: flow type (e.g., control flow)
* $W$: workflow name
* $T$: task in the workflow $W$

Architecture: Workflow $W$ with task $T$ (and possibly other). There is at least one conditional link in flow $F$ into or before task $T$ such that for any initial situation, task $T$ is executed.

Question: Will the task $T$ be executed in every possible initial situation?

Reference answer: yes

Evaluation metric: correctness

## Basic functionality patterns

In the source code and raw results, these patterns are labeled `semantics`.

### Describe task functionality

Rationale: Can the LLM determine the meaning of a task based on its name, parameters, links to other tasks, ...?

*Pattern details to be added.*

### Inconsistent task name and description

Rationale: Can the LLM detect inconsistency of a task's name and its description?

Parameters:

* $W$: workflow name
* $T$: task name
* $D_T$: task description that is inconsistent with name $T$

Architecture: Workflow $W$ with task $T$ that has a description $D_T$

Question: Identify tasks in $W$, whose name does not correspond with their description.

Reference answer: The description of task $T$ does not correspond with its name. *(exact formulation might depend on the test instance)*

Evaluation metric: ROUGE or BERTScore

Example instance: Task named 'BinaryClassificationModelTraining' with description 'Training of a regression ML model'

---

### Inconsistent task name and other entities

Rationale: Can the LLM detect inconsistencies of task's name and the linked entities (e.g., data, other tasks)?

*Pattern details to be added.*

### Meaning (functionality) of tasks

Rationale: Can the LLM interpret the meaning  of tasks adequately (e.g., task performs an operation that is not directly mentioned in its name)?

Parameters:

* $W$: workflow name
* $P$: property of task (e.g., the task is part of data preprocessing)
* $T$: task in $W$ with property $P$

Architecture: Workflow $W$ containing task $T$ (and possibly other). Property $P$ is mentioned in description/specification of $T$.

Question: Is there a task with property $P$ in workflow $W$?

Reference answer: yes

Evaluation metric: correctness

Example instance: Task 'FeatureExtraction' is labeled as "data preprocessing", question: "Is there a data processing task in 'MLTrainingAndEvaluation'?"

---

Rationale: Can the LLM interpret the meaning  of tasks adequately (e.g., task performs an operation that is not directly mentioned in its name)? (negative test)

Parameters:

* $W$: workflow name
* $P$: property of task (e.g., the task is part of data preprocessing)

Architecture: Workflow $W$ containing tasks, none of which satisfies property $P$ (it is not mentioned in description/specification of tasks).

Question: Is there a task with property $P$ in workflow $W$?

Reference answer: no

Evaluation metric: correctness

---

### Describe workflow functionality

Rationale: Can the LLM determine the meaning of a workflow based on its tasks?

*Pattern details to be added.*

### Inconsistent workflow name and description

Rationale: Can the LLM detect inconsistent workflow name and description?

Parameters:

* $W$: workflow name
* $D_W$: workflow description that is inconsistent with name $W$

Architecture: Workflow $W$ that has a description $D_W$

Question: Does the name of workflow $W$ correspond with its description? Explain your answer.

Reference answer: The description of $W$ does not correspond with its name. *(exact formulation might depend on the test instance)*

Evaluation metric: ROUGE or BERTScore

Example instance: Workflow named 'BinaryClassification' with description 'Training and evaluation of a regression ML model'

---

### Inconsistent descriptions of workflow and tasks

Rationale: Can the LLM detect inconsistent descriptions of a workflow and its tasks?

Parameters:

* $W$: workflow name
* $D_W$: workflow description
* $D_T$: task description that is inconsistent with $D_W$

Architecture: Workflow containing a task with inconsistent description.

Question: Identify tasks in workflow $W$, whose description does not correspond with the workflow description.

Reference answer: *description of the inconsistency (depends on the test instance)*

Evaluation metric: ROUGE or BERTScore

Example instance: A workflow specifying an ML pipeline where the ML goal is said to be "binary classification" in the workflow description. At the same time, the tasks perform training of a "regression" ML model (which is inconsistent with "binary classification").

---

### Semantically incorrect order of tasks

Rationale: Can the LLM detect tasks that are clearly in the wrong order (semantically)?

Parameters:

* $W$: workflow name
* $T_1, T_2$: tasks in $W$
* $F$: flow type (e.g., control flow)

Architecture: Workflow $W$ containing tasks $T_1, T_2$ (and possibly other). In flow $F$, the link $T_1 \to T_2$ is semantically incorrect.

Question: Identify potential errors in the specification of $W$ and present a list of them.

Reference answer: Task $T_2$ should precede task $T_1$ in flow $F$. *(concrete formulation depends on the test instance)*

Evaluation metric: ROUGE or BERTScore

Example instance: Workflow with task 'MLModelTraining' after 'MLModelEvaluation'.

---

### Meaning (functionality) of preceding tasks

Rationale: Can the LLM understand the meaning of tasks (e.g., a task performs an operation that is not directly mentioned in its name)?

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

### Open-ended questions

* [**ROUGE**](https://aclanthology.org/W04-1013/) (Recall-Oriented Understudy for Gisting Evaluation): the word overlap of the reference answer and the LLM output
* [**BERTScore**](https://arxiv.org/abs/1904.09675): the cosine similarity of word embeddings (that capture the meaning of words)
* **manual**: manual assessment of the LLM's output
* **LLM as a judge** (e.g., [G-Eval](https://arxiv.org/abs/2303.16634)): use another LLM to assess the LLM's output
