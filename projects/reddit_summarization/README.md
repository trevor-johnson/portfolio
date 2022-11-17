# Reddit TLDR Abstractive Summarization Model

For my final project in my Natural Language Processing class at UC Berkeley, a classmate and I created an NLP model that generates abstractive summaries of long Reddit posts. To do so, we began with a dataset of Reddit posts that already had a TLDR written by the author. With this dataset, we trained a BART model using PyTorch to generate fluent and faithful summaries for long Reddit posts. Furthermore, we trained separate BART models on genre-specific posts by using the subreddits as categories. In almost all cases, we find a model trained on a larger generalized dataset produces higher ROUGE scores than comparable models trained on smaller specialized datasets. The results are formally documented in a research paper.

While this was a group project, all code in this repository is my own.

## Links

- [Research paper](https://github.com/trevor-johnson/portfolio/blob/main/projects/reddit_summarization/final_paper/final_paper.pdf)
- [My fine tuned Reddit BART model on Huggingface](https://huggingface.co/trevorj/BART_reddit)
- [Reddit dataset](https://huggingface.co/datasets/reddit)