# SPIQA (Scientific Paper Image Question Answering)


**Date**: 2024-07-12


**Name**: SPIQA  Scientific Paper Image Question Answering 


**Domain**: Computer Science


**Focus**: Multimodal QA on scientific figures


**Keywords**: multimodal QA, figure understanding, table comprehension, chain-of-thought


**Task Types**: Question answering, Multimodal QA, Chain-of-Thought evaluation


**Metrics**: Accuracy, F1 score


**Models**: Chain-of-Thought models, Multimodal QA systems


**Citation**:


- Xiaoyan Zhong, Yijian Gao, and Suchin Gururangan. Spiqa: scientific paper image question answering. 2024. URL: https://arxiv.org/abs/2407.09413.

  - bibtex: |

      @misc{zhong2024spiqa,

        title={SPIQA: Scientific Paper Image Question Answering},

        author={Zhong, Xiaoyan and Gao, Yijian and Gururangan, Suchin},

        year={2024},

        url={https://arxiv.org/abs/2407.09413}

      }



**Ratings:**


Specification:


  - **Rating:** 10


  - **Reason:** Task administration clearly defined; prompt instructions explicitly given, no ambiguity in format or scope. 


Dataset:


  - **Rating:** 9


  - **Reason:** Dataset is available  via paper/appendix , includes train/test/valid split. FAIR-compliant with minor gaps in versioning or access standardization. 


Metrics:


  - **Rating:** 9


  - **Reason:** Uses quantitative metrics  Accuracy, F1  aligned with the task. Well-suited for benchmarking multimodal reasoning. 


Reference Solution:


  - **Rating:** 5


  - **Reason:** Multiple model results  e.g., GPT-4V, Gemini  reported; baselines exist, but full runnable code not confirmed for all. 


Documentation:


  - **Rating:** 2


  - **Reason:** Dataset and benchmark description provided; code/software mentioned; however, full step-by-step setup or containerized environment not stated. 


**Radar Plot:**
 ![Spiqa Scientific Paper Image Question Answering radar plot](../../tex/images/spiqa_scientific_paper_image_question_answering_radar.png)