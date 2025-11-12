# Presentation

## Title Slide

<!-- EMPTY -->

## Introduction

Today I'm going to cover the topic of fine-tuning large language models focussing on two parameter efficient methods called LoRA and QLoRA.

LLMs have rapidly become useful in many fields, including at Lendable, due to their effectiveness in tackling a variety of problems. These involve classification, content generation, and many other capabilities straight off the shelf. These capabilities come from training regimes focussing on a wide breadth of data, however, this can mean that LLMs are not always well suited for tasks focussed on specific domains or use cases due to their generalised training regime. As a result, sometimes we may seek to adjust these models to specific roles and tasks, and this is where fine-tuning comes into play.

## Fine Tuning

> Fine-tuning an LLM is the process of adapting a pre-trained model to perform better at a specific task.

Naive fine-tuning is the relatively simple approach of taking an existing model, and continuing its training regime with the models trained weights as a starting point.
This involves updating ALL of the parameters of the model with full forwards and backpropogation passes to update the weights. This makes fine-tuning very large models extremely inefficient.
Some approaches involve limiting the weights being updated or training external modules to adapt the model for a specific task, but these approaches fail to reach the naive fine-tuning baseline performnce. In addition they often introduce inference latency or reduce the models usable context window.

The diagrams shown are a simplification but appraoches which add adapter layers to the model must be run in sequence breaking the parallelism of the deep models and prompt engineering style prefix layer appraoches suffer from decreasing context windows and performance gains which are hard to map to trainable parameters.

A method of fine-tuning which doesn't suffer from these drawbacks and also attains the naive fine-tuning baseline is LoRA.

## LoRA

LoRA takes inspiration from a paper showing that over-parametrised models such as LLMs have a low intrinsic dimesnion. The approach of this paper from Microsoft hypothesises that when fine-tuning a model, the change in weights that occurs has a low intrinsic rank, hence the name Low Rank Adaptation.
This hypothesis means that you don't have to train a models weights directly, but instead a low rank representation of the CHANGES to those weights. This means you don:t have to track changes to all the weights of the model making this fine-tuning much more memory and compute efficient.
<!-- TODO: Animation here showing LoRA breakdown from existing -->

<!-- TODO: -->

### LoRA: Advantages and Disadvantages

#### Advantages (LoRA)

- LoRA is a true generalisation of fine tuning in a manner which additional layers and prefix based methods aren't. Increasing the rank $r$ eventually converges to training the original model.
- It has no inference latency as we can easily calculate $W_0 + BA$ at inference time and easily change our model weights to those of a different fine-tuned model with $W_0 + B'A'$
<!-- TODO: Do animation of W_0 -->
- This decomposition also makes the weight updates more interpretable in relation to the overall model weights
- Furthermore, the paper finds that even extremely low ranks such as 1 or 2 are sufficient to attain strong fine-tuning performance for large performance gains

#### Drawbacks (LoRA)

- Deciding

### LoRA: Performance

<!-- TODO: -->

<!-- TODO: Discussion of extra paper stuff goes here -->

## QLoRA

<!-- TODO: -->

### QLoRA: Advantages and Disadvantages

#### Advantages (QLoRA)

<!-- TODO: -->

#### Drawbacks (QLoRA)

<!-- TODO: -->

### QLoRA: Performance

<!-- TODO: -->

## Discussion Points

1. <!-- TODO: -->
2. <!-- TODO: -->
3. <!-- TODO: -->

## Questions

Any questions?
