# Reading list: Hindi-English code-switching and tokenizer study

Curated 7 November 2026. The links point to publisher or author-maintained pages. Where a PDF is available, the paper page normally links to it. This list is intended to seed the Drive reading folder, not to replace a full literature review.

## Start here

1. **Doddapaneni et al. (2023), “Towards Leaving No Indic Language Behind.”** Read for IndicCorp, IndicXTREME, IndicBERT v2, language coverage, evaluation construction, and its tokenizer-fertility analysis. Fertility is a diagnostic in this broad resources paper, not a causal explanation of model gaps. [ACL Anthology paper and PDF](https://aclanthology.org/2023.acl-long.693/)
2. **Singh et al. (2024), “IndicGenBench.”** Read for generation evaluation across 29 Indic languages, prompting and transfer settings, qualitative errors, and the connection between token fertility and context-window/example capacity. Its OpenAI BPE analysis does not establish causal effects for each evaluated model. [ACL Anthology paper and PDF](https://aclanthology.org/2024.acl-long.595/)
3. **Mohamed et al. (2026), “Lost in the Mix: Evaluating LLM Understanding of Code-Switched Text.”** Read this for the controlled benchmark design, ECT/MLF-constrained noun switching, paired accuracy contrasts, and the limits of LLM-generated stimuli. The paper does not measure tokenizer fragmentation. [ACL Anthology paper and PDF](https://aclanthology.org/2026.acl-long.2080/)
4. **Dwivedi and Gopalan (2026), “Comparative Analysis of the Intrinsic Metrics for Tokenizers and their effect on Downstream Tasks for Hindi and Marathi.”** Closest direct work for Hindi/Marathi tokenizers and intrinsic metrics; it includes fertility, Rényi efficiency, percentile frequency, and downstream tasks. Its results motivate an extension, but do not substitute for this study's code-switched reasoning evaluation. [ACL Anthology paper and PDF](https://aclanthology.org/2026.acl-long.1037/)
5. **Ravikiran et al. (2026), “Do Tokenizers Fail on Informal Hindi Expressions? Evidence from Static, Downstream, and Robustness Analyses.”** Read for informal Hindi, Romanization, spelling variation, and phrase-boundary measures. [ACL Anthology paper and PDF](https://aclanthology.org/2026.loreslm-1.2/)
4. **Altıntaş et al. (2026), “TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior.”** Useful for understanding what a stronger tokenizer-causality design looks like when training conditions are controlled. The current cross-model pilot cannot make a causal tokenizer claim. [PMLR paper](https://proceedings.mlr.press/v306/altintas26a.html)
5. **Ali et al. (2024), “Tokenizer Choice for LLM Training: Negligible or Crucial?”** Controlled training comparisons show that fertility and parity are not reliable stand-alone predictors of downstream quality. [Findings of NAACL paper and PDF](https://aclanthology.org/2024.findings-naacl.247/)

## Tokenizer metrics and multilingual fairness

- **Rust et al. (2021), “How Good Is Your Tokenizer? On the Monolingual Performance of Multilingual Language Models.”** Background on multilingual tokenizer evaluation and fertility. [ACL Anthology](https://aclanthology.org/2021.acl-long.243/)
- **Petrov et al. (2023), “Language Model Tokenizers Introduce Unfairness Between Languages.”** Motivates measuring token burden and its downstream implications across languages. [NeurIPS paper](https://proceedings.neurips.cc/paper_files/paper/2023/file/74bb24dca8334adce292883b4b651eda-Paper-Conference.pdf)
- **Chiu (2026), “TokLens: A Multilingual Lens on Tokenizer Quality for LLMs.”** Broader intrinsic metric set, including single-token retention and token cost measures. [ACL Anthology](https://aclanthology.org/2026.acl-srw.18/)
- **Kumar et al. (2024), “Evaluating Tokenizer Performance of Large Language Models Across Official Indian Languages.”** Wide Indic-language comparison for later language expansion. [arXiv](https://arxiv.org/abs/2411.12240)
- **Pires et al. (2024), “Improving Bengali and Hindi Large Language Models.”** Compares tokenization choices for Hindi and Bengali downstream work. [LREC-COLING paper and PDF](https://aclanthology.org/2024.lrec-main.764/)
- **Rana et al. (2025), “IndicSuperTokenizer: An Optimized Tokenizer for Indic Multilingual LLMs.”** Indic-focused tokenizer proposal and evaluation across 22 Indian languages. Treat this as a preprint and verify its publication status before citing it as peer reviewed. [arXiv preprint](https://arxiv.org/abs/2511.03237)
- **Brahma et al. (2026), “Multilingual Tokenization through the Lens of Indian Languages: Challenges and Insights.”** Recent broad comparison of tokenization across 17 Indic languages and 11 scripts. [Findings of ACL paper](https://aclanthology.org/2026.findings-acl.1632/)
- **Gambäck and Das (2016), “Code-Mixing: A Challenge for Language Identification in the Language of Social Media.”** Source for the Code-Mixing Index; CMI does not measure grammaticality or naturalness. [ACL Anthology](https://aclanthology.org/L16-1292/)

## Code-switching and Romanization

- **Yang and Chai (2025), “CodeMixBench: A Multilingual Code-Mixing Benchmark.”** Candidate external benchmark for a later validation phase. [EMNLP paper](https://aclanthology.org/2025.emnlp-main.109/)
- **Winata et al. (2026), “CodeMixQA.”** Human-annotated parallel code-switched QA with script variants; investigate dataset fit and license before reuse. [arXiv](https://arxiv.org/abs/2601.07153)
- **Das et al. (2026), “Indi-RomCoM.”** Romanized Indic-English instructions and mixing intensity. It complements, rather than replaces, the matched script contrast. [arXiv](https://arxiv.org/abs/2606.30790)
- **Kodali et al. (2022), “SyMCoM: Syntactic Measure of Code Mixing.”** A syntactic descriptor that can complement CMI and switch-point counts. [Findings of ACL](https://aclanthology.org/2022.findings-acl.40/)
- **Gautam (2026), “LIPI: Transliterating Hindi the Way People Type It.”** Motivation for treating naturally typed Romanized Hindi and spelling variation as study factors. [WAT paper](https://aclanthology.org/2026.wat-1.2/)

## New ideas that could be preregistered for a later study

1. Add spelling-variant robustness for Romanized Hindi, holding meaning and switch location constant.
2. Add an external naturalistic code-mixed dataset after the controlled A/B/C study.
3. Consider Rényi efficiency or percentile frequency as secondary tokenizer metrics, then predefine their exact formulas and analysis before collecting outcomes.
4. Replicate the matched script design with Marathi before moving to distinct South Indian language families. Preserve separate native-script and Romanized measures.
5. For tokenizer causality, use a controlled training study or a resource such as TokSuite where model training variables are held fixed. Comparing unrelated pretrained models supports only association.

## Model papers and official cards

- [Llama 3.1 8B Instruct model card](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)
- [Qwen3 8B model card and tokenizer files](https://huggingface.co/Qwen/Qwen3-8B)
- [Gemma 3 4B Instruct model card](https://huggingface.co/google/gemma-3-4b-it)
- [Mistral 7B Instruct v0.3 model card and tokenizer files](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3)
- [DeepSeek R1 Distill Qwen 7B model card](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B)
- [Sarvam-M model card and tokenizer files](https://huggingface.co/sarvamai/sarvam-m)

