# MMLU (Massive Multitask Language Understanding)


**Date**: 2020-09-07


**Name**: MMLU  Massive Multitask Language Understanding 


**Domain**: Multidomain


**Focus**: Academic knowledge and reasoning across 57 subjects


**Keywords**: multitask, multiple-choice, zero-shot, few-shot, knowledge probing


**Task Types**: Multiple choice


**Metrics**: Accuracy


**Models**: GPT-4o, Gemini 1.5 Pro, o1, DeepSeek-R1


**Citation**:


- Dan Hendrycks, Collin Burns, and Saurav Kadavath. Measuring massive multitask language understanding. 2021. URL: https://arxiv.org/abs/2009.03300.

  - bibtex: |

      @misc{hendrycks2021measuring,

        title={Measuring Massive Multitask Language Understanding},

        author={Hendrycks, Dan and Burns, Collin and Kadavath, Saurav},

        journal={arXiv preprint arXiv:2009.03300},

        year={2021},

        url={https://arxiv.org/abs/2009.03300}

      }



**Ratings:**


Specification:


  - **Rating:** 9


  - **Reason:** Clearly defined method of giving inputs, although it lacks hardware specifications. 


Dataset:


  - **Rating:** 9


  - **Reason:** Contains predefined few-shot development, validation, and testing set. Easy to access and download, but not versioned. 


Metrics:


  - **Rating:** 9


  - **Reason:** Clearly defined primary metric of number of multiple-choice questions answered correctly. Secondary metric of confidence requires models to self-report. 


Reference Solution:


  - **Rating:** 10


  - **Reason:** Performance and links to several top models linked on the Github. 


Documentation:


  - **Rating:** 8


  - **Reason:** Code and datasets provided and easy to find, but no environment setup instructions given. 


**Radar Plot:**
 ![Mmlu Massive Multitask Language Understanding radar plot](../../tex/images/mmlu_massive_multitask_language_understanding_radar.png)