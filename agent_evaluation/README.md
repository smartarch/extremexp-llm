# LLM Evaluation

This folder contains sample test instances for evaluating a LLM-based Agent. The instances are manually created based on the [*test instance patterns*](/patterns.md).

The evaluation can be run via the [`main.py`](main.py) file (assuming the necessary dependencies were installed as instructed in [installation](/README.md#Installation)).

The test instances depend on the architecture specifications defined in the [`examples`](/examples/) folder. There are currently three variants of the architecture specification DSL to test. The desired variant is set by the `variant` variable in the [`main.py`](main.py) file.

## DSL Variants

### Variant 1: Inheritance (also known as `separate files`)

The first variant is the DSL developed for the XXP project. In this variant, there can be workflows derived from other workflows. In the derived workflow (called *assembled* in the project), the configuration of the tasks can be updated, but no new control flow or data flow can be added. To fully understand the derived workflow (especially to be able to reason about the control and data flow), it is necessary to obtain the specification of the base workflow (which is referenced from the derived workflow).

The tasks can either be *primitive* (an implementation file is specified) or *composite* (composed of other tasks). For the composite tasks, a reference to a sub-workflow is specified where the sub-tasks are defined.

An example workflow specification can be found in the [`/examples/artificial_workflow/1_separate_files`](/examples/artificial_workflow/1_separate_files/) folder.

### Variant 2: Inlined (a.k.a. `assembled`)

The second variant is a simplified version of the first variant, where only *assembled* workflows exist. Instead of referencing the base workflow, all the information are copied into the specification of the derived workflow (and slightly syntactically simplified).

An example workflow specification can be found in the [`/examples/artificial_workflow/2_assembled`](/examples/artificial_workflow/2_assembled/) folder.

### Variant 3: No sub-workflows (a.k.a. `expanded`)

The third variant is created from the second variant by inlining all the sub-workflows. Instead of a reference to a sub-workflow, the whole specification is copied inside the composite task. This can lead to a high level of nesting of tasks.

An example workflow specification can be found in the [`/examples/artificial_workflow/3_expanded`](/examples/artificial_workflow/3_expanded/) folder.

## Results summary

We manually created 25 test instances based on the [*test patterns*](/patterns.md). The table summarizes score for each pattern and variant by $\textit{mean}\pm\textit{std}$ of 5 repetitions of the experiment.

Note: The *Basic functionality* patterns are labeled `semantics` in the source code and raw results.

### GPT-4o (`gpt-4o-2024-05-13`) Agent

The LLM has to ask for workflow specifications.

| **Pattern category**  | **Pattern name**                     | **Number of instances** | **Variant 1 Score** | **Variant 2 Score** | **Variant 3 Score** |
|-----------------------|--------------------------------------|-------------------------|---------------------|---------------------|---------------------|
| Structure | List of tasks                                    | 5                       | $0.85\pm0.00$       | $1.00\pm0.00$       | $1.00\pm0.00$       |
| Structure | Links in flow                                    | 4                       | $0.95\pm0.11$       | $0.95\pm0.11$       | $0.95\pm0.11$       |
| Structure | Task after task                                  | 4                       | $0.75\pm0.18$       | $0.85\pm0.14$       | $0.70\pm0.11$       |
| Structure | Next tasks in flow                               | 4                       | $0.95\pm0.11$       | $0.90\pm0.14$       | $0.78\pm0.14$       |
| Structure | Flow cycle                                       | 4                       | $0.80\pm0.11$       | $1.00\pm0.00$       | $0.70\pm0.11$       |
| Structure | *Total*                                          | *21*                    | $0.86\pm0.05$       | $0.94\pm0.06$       | $0.83\pm0.03$       |
| Behavior  | Mutually exclusive conditional flow              | 2                       | $1.00\pm0.00$       | $1.00\pm0.00$       | $1.00\pm0.00$       |
| Behavior  | *Total*                                          | *2*                     | $1.00\pm0.00$       | $1.00\pm0.00$       | $1.00\pm0.00$       |
| Basic functionality | Inconsistent task name and description | 1                       | $0.76\pm0.07$       | $0.72\pm0.08$       | $0.73\pm0.04$       |
| Basic functionality | Inconsistent descriptions              | 1                       | $0.79\pm0.04$       | $0.81\pm0.03$       | $0.77\pm0.05$       |
| Basic functionality | *Total*                                | *2*                     | $0.77\pm0.04$       | $0.77\pm0.04$       | $0.75\pm0.03$       |

### GPT-4o (`gpt-4o-2024-05-13`) Up Front

All workflow specifications are presented in the initial prompt.

Note that for Variant 3, it does not make it does not make sense to differentiate between *agent* and *up front* modes as there is always only one WADL specification file.

| **Pattern category**  | **Pattern name**                     | **Number of instances** | **Variant 1 Score** | **Variant 2 Score** |
|-----------------------|--------------------------------------|-------------------------|---------------------|---------------------|
| Structure | List of tasks                                    | 5                       | $0.95\pm0.12$       | $1.00\pm0.00$       |
| Structure | Links in flow                                    | 4                       | $1.00\pm0.00$       | $1.00\pm0.00$       |
| Structure | Task after task                                  | 4                       | $0.95\pm0.11$       | $1.00\pm0.00$       |
| Structure | Next tasks in flow                               | 4                       | $0.80\pm0.11$       | $0.88\pm0.12$       |
| Structure | Flow cycle                                       | 4                       | $1.00\pm0.00$       | $1.00\pm0.00$       |
| Structure | *Total*                                          | *21*                    | $0.94\pm0.04$       | $0.98\pm0.02$       |
| Behavior  | Mutually exclusive conditional flow              | 2                       | $1.00\pm0.00$       | $1.00\pm0.00$       |
| Behavior  | *Total*                                          | *2*                     | $1.00\pm0.00$       | $1.00\pm0.00$       |
| Basic functionality | Inconsistent task name and description | 1                       | TODO                | TODO                |
| Basic functionality | Inconsistent descriptions              | 1                       | TODO                | TODO                |
| Basic functionality | *Total*                                | *2*                     | TODO                | TODO                |

### GPT-4 Turbo (`gpt-4-0125-preview`) Agent

The LLM has to ask for workflow specifications.

| **Pattern category**  | **Pattern name**                     | **Number of instances** | **Variant 1 Score** | **Variant 2 Score** | **Variant 3 Score** |
|-----------------------|--------------------------------------|-------------------------|---------------------|---------------------|---------------------|
| Structure | List of tasks                                    | 5                       | $0.85\pm0.00$       | $1.00\pm0.00$       | $1.00\pm0.00$       |
| Structure | Links in flow                                    | 4                       | $0.95\pm0.11$       | $1.00\pm0.00$       | $0.85\pm0.22$       |
| Structure | Task after task                                  | 4                       | $0.60\pm0.14$       | $0.75\pm0.00$       | $0.60\pm0.14$       |
| Structure | Next tasks in flow                               | 4                       | $1.00\pm0.00$       | $1.00\pm0.00$       | $1.00\pm0.00$       |
| Structure | Flow cycle                                       | 4                       | $0.85\pm0.14$       | $1.00\pm0.00$       | $1.00\pm0.00$       |
| Structure | *Total*                                          | *21*                    | $0.85\pm0.04$       | $0.95\pm0.00$       | $0.90\pm0.04$       |
| Behavior  | Mutually exclusive conditional flow              | 2                       | $1.00\pm0.00$       | $1.00\pm0.00$       | $1.00\pm0.00$       |
| Behavior  | *Total*                                          | *2*                     | $1.00\pm0.00$       | $1.00\pm0.00$       | $1.00\pm0.00$       |
| Basic functionality | Inconsistent task name and description | 1                       | $0.65\pm0.02$       | $0.54\pm0.10$       | $0.70\pm0.06$       |
| Basic functionality | Inconsistent descriptions              | 1                       | $0.82\pm0.03$       | $0.80\pm0.02$       | $0.80\pm0.07$       |
| Basic functionality | *Total*                                | *2*                     | $0.74\pm0.01$       | $0.67\pm0.04$       | $0.75\pm0.06$       |



## Discussion

### Stochasticity

It should be noted that the responses of LLMs are stochastic; thus running the experiment with the same test instances again may produce slightly different results.

### Exact question formulation

We noticed that it is necessary to formulate the questions as exactly as possible. For example, when the LLM is asked to "list all tasks that have a parameter", it sometimes also lists tasks that depend on the `Hyperparameters` data object. However, when we improved the question by adding "(specified via the 'param' keyword)", we got the answers we wanted.

Another example is the "Links in flow" and "Task after task" patterns. Although they technically ask about the same workflow feature (control flow links), the question is formulated differently, and the results differ. Interestingly, the test instance that scored the worst was asking whether `ModelTraining` task is "directly after" `ModelEvaluation` task in the control flow (the order was intentionally semantically incorrect in the specification). On the other hand, the LLM answers mostly correctly if the question is formulated whether there "is a control flow link" between the tasks.

### LLM requests the necessary workflow specifications

In our evaluation setup, we do not present the workflow specifications to the LLM in the initial prompt. Rather, the LLM works as an agent (based on the [ReAct](https://arxiv.org/abs/2210.03629) approach and [function calling](https://platform.openai.com/docs/guides/function-calling)) and can request the workflow specification files it needs. We chose this approach because we wanted to see whether the LLM is able to choose which information is necessary. This is aligned with our long-term goal of building an assistant that could also work, for example, with experiment results, and always presenting all the available information to the LLM can become costly.

### Evaluation of open-ended questions (basic functionality patterns)

We evaluated all the basic functionality patterns using the recall from [ROUGE-1 metric](https://aclanthology.org/W04-1013/). In short, this counts how many words from the reference answer appeared in the LLM's answer. Clearly, this metric depends on the concrete formulation of the answer so a correct answer formulated in different words will not get a perfect score. For reference, we also checked all the answers by hand and the LLM's responses contained the correct answer for all the basic functionality instances. That means that the scores for semantic patterns in table above correspond to correct answers.

It should also be noted that even a wrong answer would score well in the ROUGE-1 metric if it contained all the words from the reference answer (possibly in incorrect order or with different meanings). Further investigation is necessary to assess whether other metrics (e.g., [BERTScore](https://arxiv.org/abs/1904.09675), [G-Eval](https://arxiv.org/abs/2303.16634)) are more appropriate for evaluating open questions.

### Chain of thought

We noticed that the LLM performed significantly better when the [chain of thought](https://arxiv.org/abs/2205.11916) technique was applied. We asked the LLM to first think about the answer and explain it, and then submit the final answer.

There is no guarantee that the explanation will correspond to the answer, but it can give us insights into why the LLM does not understand a particular type of question. For instance, it can show us that the LLM cannot interpret parts of the DSL correctly and understands it differently than we meant.

This can be taken one step further by asking the LLM what information it needs to know to answer the question. Again, giving that information to the LLM is not guaranteed to improve the answer, but it can at least give us ideas on what to try.

### Cost

In our setup (LLM inputs: system prompt with general information, specification of workflow in our DSL, test instance question; LLM outputs: answer to the test instance, explanation of the answer; LLM model: GPT-4 Turbo), the cost of running the evaluation is roughly 0.02 USD per test instance.

### Time

In our setup, it takes approximately 10 seconds to process one test instance. That totals to approximately 4-5 minutes for the evaluation with 25 test instances.
