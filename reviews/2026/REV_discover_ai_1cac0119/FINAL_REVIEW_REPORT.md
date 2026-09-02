# PEER REVIEW REPORT: SPRINGER NATURE DISCOVER JOURNALS
> **Journal:** Discover Artificial Intelligence  
> **Manuscript ID:** 1cac0119-f585-45d1-87aa-65c7fecddf40  
> **Article Title:** Learning Analytics for Detecting Digital Information Overload Among Postgraduate Students Using Machine Learning  
> **Submission Round:** Revised Submission (Post Minor Revision)  
> **Guideline Reference:** https://link.springer.com/brands/discover/for-reviewers

---

## PART 1: COMMENTS TO THE AUTHOR(S)

### 1. Key Results & Summary of the Work
The manuscript investigates the detection of Digital Information Overload (DIO) among postgraduate students using text analysis of 100 questionnaire responses collected at Nigerian universities. The authors formulate a data-centric machine learning pipeline combining text preprocessing, TF-IDF feature extraction, threshold-based keyword labeling, and four supervised classifiers (Logistic Regression, Support Vector Machine, Naïve Bayes, and Random Forest). Experimental results report 90% accuracy with SVM and 85% with Random Forest and Naïve Bayes on a 20-sample test set. 

In accordance with Discover’s editorial criteria, this evaluation focuses exclusively on methodological soundness, experimental transparency, and accurate reporting of results, rather than subjective novelty or perceived significance.

### 2. Methodological Rigor & Data Quality
* **Experimental Pipeline:** The use of classical machine learning algorithms paired with TF-IDF vectorization is well-suited for a small-scale exploratory text dataset ($N=100$) where deep neural networks would be prone to extreme overfitting.
* **Synthetic Data Disclosure:** Section 3.1.1 mentions that a proportion of synthetically augmented samples was introduced to balance the initial 90:10 class imbalance to 56:44. However, the exact number of synthetic samples (e.g., how many of the 44 Low/Moderate instances were synthesized), the generation algorithm (e.g., synonym replacement, back-translation, or LLM-based prompting), and whether augmentation occurred before or after the train–test split are not specified. Please clarify these details to rule out data leakage and ensure reproducibility.

### 3. Statistics, Uncertainties & Figure Legends
* **Sample Size & Overclaiming:** The independent test set contains 20 samples ($20\%$ of $100$). On a test set of this size, the difference between SVM ($90\% = 18/20$), Random Forest ($85\% = 17/20$), and Naïve Bayes ($85\% = 17/20$) corresponds to literally a single sample misclassification ($5\%$). While SVM performed well, claiming that it *"consistently outperforms other models... indicating superior classification capability"* overstates the statistical confidence of a one-sample variance. Please soften this statement to acknowledge that the performance differences among SVM, RF, and NB are marginal and exploratory.
* **Figure Legends & Error Bars:** 
  - Figure 2: In line with Discover journal guidelines, please include error bars representing fold-level variance (e.g., from the 5-fold cross-validation) in the bar chart, or explicitly direct readers to the standard deviations reported in Section 4.1.
  - Figure 3 (Confusion Matrix): The axes currently display raw continuous coordinate numbers (`-0.50, 0.00, 0.50, 1.00, 1.50`). Please replace these with the actual categorical class labels (`High Overload`, `Low/Moderate`) to improve visual clarity.

### 4. Interpretation of Data, Labeling Logic & Limitations
* **Feature Importance vs. Labeling Circularity:** In Section 3.4, the authors used keywords such as *stress*, *overload*, and *distraction* to compute document scores for label assignment. In Section 4.4, Random Forest identified these exact terms as the most important features. Interpreting this outcome as proof that the model *"validated the selected features"* represents circular reasoning, since the classifier simply learned the explicit rules used to create the ground truth. Please rephrase this discussion to explain that the feature importance confirms the classifier effectively captured the rule-based labeling heuristic, rather than discovering an independent latent construct.
* **Empirical Support for Word2Vec Comparison:** Section 5.2 provides an interesting qualitative discussion on *"Why Word2Vec Failed"*, but neither Table 3 nor the text provides the quantitative performance metrics (Accuracy, F1) achieved by the Word2Vec baseline. Please report the numerical scores obtained by the Word2Vec experiments, and specify whether pre-trained embeddings or domain-trained embeddings were evaluated.

### 5. Ethical Guidelines (SAGER) & References
* **SAGER Compliance:** The study surveyed human participants (postgraduate students). To align with the Sex and Gender in Research (SAGER) guidelines recommended by Discover, please briefly state in Section 3.1 whether participant sex or gender data were collected, or note the absence of gender-disaggregated analysis as a limitation.
* **Ethical Approval:** The authors have satisfactorily incorporated the formal ethical approval statement (`ABUCUHSR/2025/023`, Ahmadu Bello University) in the revised draft, resolving the prior concern.

### 6. Essential Revisions & Actionable Suggestions
1. **Clarify Synthetic Augmentation:** State the exact number of synthetic samples, the generation method used, and confirm that augmentation was performed strictly within the training set.
2. **Calibrate Model Comparison Language:** Moderate claims regarding the "superiority" of SVM over Random Forest and Naïve Bayes in Sections 1, 4.2, 4.3, and 7, highlighting that the one-sample difference on $n=20$ reflects exploratory parity rather than definitive statistical dominance.
3. **Refine Figure 3:** Label the confusion matrix axes with proper class names rather than numeric array bounds.
4. **Supply Word2Vec Metrics:** Include the baseline accuracy/F1 numbers for Word2Vec in Section 5.2 or Table 3 to substantiate the comparative discussion.

---

## PART 2: CONFIDENTIAL COMMENTS TO THE EDITOR

### 1. Overall Recommendation
**Minor Revision (Essential Clarifications)**

### 2. Frank Technical Assessment to the Handling Editor
The authors have addressed the ethical documentation requirement raised in the previous minor revision round by integrating the institutional ethics approval from Ahmadu Bello University (`ABUCUHSR/2025/023`).

Scientifically, this exploratory paper aligns with Discover AI's "Sound Science" publishing remit: it addresses an important educational issue (digital information overload) using an appropriate, interpretable classical NLP pipeline on qualitative survey data. The authors are honest about the small sample size ($N=100$) in their Limitations section. 

The remaining issues are technical and editorial:
1. The authors should clarify the proportion and methodology of synthetic data augmentation to ensure no data leakage occurred into the test set.
2. The claim of SVM "superiority" over Random Forest/Naïve Bayes is an overstatement given that the test set consists of only 20 samples (a single sample difference accounts for 5%).
3. Figure 3 needs proper axis labels, and numerical metrics should accompany the discussion of Word2Vec.

These adjustments are straightforward and feasible within a short revision timeframe (under 10 days), after which the manuscript should be acceptable for publication.

### 3. Scope of Assessment
Full technical assessment completed across text preprocessing, feature extraction, ML classifiers, evaluation metrics, and ethics compliance.

### 4. Mandatory AI Policy Disclosure Statement
*In compliance with Springer Nature's policy on AI use by peer reviewers:*
- [x] **Option B:** Generative AI was used strictly and solely for grammar and language editing of the reviewer's own independently drafted assessment. No manuscript content, confidential extracts, or raw data were uploaded into any public generative AI tool.