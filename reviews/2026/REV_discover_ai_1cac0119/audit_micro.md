# MICRO TECHNICAL AUDIT: DEEP METHODOLOGICAL SCRUTINY
> **Manuscript ID:** 1cac0119-f585-45d1-87aa-65c7fecddf40  
> **Title:** Learning Analytics for Detecting Digital Information Overload Among Postgraduate Students Using Machine Learning

---

### 1. Phân tích Cỡ mẫu Thử nghiệm ($n=20$) & Nguy cơ Thổi phồng Kết luận (*Overclaiming*)
* **Hiện trạng số liệu:** Tổng mẫu $N=100$. Tỷ lệ chia tập Train/Test là $80/20$ ➔ Tập Test độc lập chỉ có đúng **20 mẫu** (khoảng 11 mẫu High Overload, 9 mẫu Low/Moderate).
* **Bản chất toán học của Bảng 3:**
  * SVM đạt độ chính xác $90\%$ ➔ Đoán đúng **18 / 20 mẫu** (sai 2 mẫu).
  * Random Forest & Naïve Bayes đạt $85\%$ ➔ Đoán đúng **17 / 20 mẫu** (sai 3 mẫu).
  * Logistic Regression đạt $80\%$ ➔ Đoán đúng **16 / 20 mẫu** (sai 4 mẫu).
* **Nhận định chuyên môn:**
  Khoảng cách giữa "mô hình xuất sắc nhất" (SVM) và hai mô hình xếp sau (RF, NB) chỉ là **đúng 1 câu trả lời** ($1/20 = 5\%$). Sự chênh lệch này hoàn toàn nằm trong biên độ ngẫu nhiên của việc lấy mẫu nhỏ. Việc tác giả khẳng định trong phần 4.2 & 4.3 rằng *"SVM consistently outperforms other models... indicating superior classification capability"* là chưa đủ căn cứ thống kê và cần được điều chỉnh giọng văn thành nhận định thăm dò (*exploratory finding*).

---

### 2. Sự Thiếu Minh bạch về Dữ liệu Tổng hợp (*Synthetic Data*) & Rủi ro Rò rỉ (*Data Leakage*)
* **Hiện trạng:**
  * Mục 3.1.1 đề cập: *"The dataset consists primarily of real questionnaire responses, with a limited proportion of synthetically augmented samples used to improve class balance."*
  * Mục 3.4 cho biết phân phối ban đầu bị lệch nghiêm trọng ($90:10$), sau đó được cân bằng lại thành $56:44$ (Tổng 100 mẫu).
* **Câu hỏi kỹ thuật then chốt chưa được giải thích:**
  1. Nếu ban đầu là $90:10$ trong 100 mẫu thật, thì lớp thiểu số chỉ có 10 mẫu. Để đạt tỷ lệ $44$ mẫu Low/Moderate, tác giả đã sinh ra bao nhiêu mẫu nhân tạo? (Có phải khoảng 34 mẫu nhân tạo, chiếm >30% tập dữ liệu?).
  2. Dữ liệu nhân tạo được sinh bằng phương pháp nào? (Prompt LLM, hoán đổi từ đồng nghĩa EDA, back-translation hay rule-based?).
  3. Quá trình sinh dữ liệu nhân tạo diễn ra **trước** hay **sau** khi chia tập Train/Test? Nếu sinh trước khi chia 80/20, đây là lỗi rò rỉ dữ liệu (*Data Leakage*) kinh điển trong ML vì dữ liệu test bị ảnh hưởng bởi quá trình sinh của tập train.

---

### 3. Vòng lặp Logic trong Phân tích Trọng số Đặc trưng (*Feature Importance Circularity*)
* **Quy trình gán nhãn (Mục 3.4):** Tác giả dùng các từ khóa (`stress`, `anxiety`, `overload`, `distraction`, `confusion`) để tính điểm $Score(d)$, nếu vượt ngưỡng $\theta$ thì gán nhãn 1 (High Overload).
* **Kết quả Random Forest (Mục 4.4, Hình 4):** Các từ quan trọng nhất được mô hình tìm ra là: `overload`, `stress`, `distraction`.
* **Vấn đề lập luận:** Tác giả viết: *"These findings validate the selected features and demonstrate the effectiveness of the model..."*  
  Đây là lập luận vòng tròn (*tautological reasoning*). Mô hình tìm thấy các từ đó là vì chính các từ đó đã được dùng làm công thức gán nhãn $y$. Cần làm rõ rằng đây là sự xác nhận mô hình đã học đúng luật gán nhãn của tác giả, chứ không phải một phát hiện ngữ nghĩa khách quan độc lập từ người học.

---

### 4. Thiếu Dữ liệu Định lượng về Thất bại của Word2Vec (Mục 5.2)
* Mục 5.2 dành hẳn 3 đoạn văn phân tích sâu lý do *"Why Word2Vec Failed"*.
* Tuy nhiên, trong toàn bộ bài báo (kể cả Bảng 3), **hoàn toàn không có bất kỳ con số nào** ghi nhận độ chính xác hay F1 của Word2Vec!
* Tác giả cần bổ sung Word2Vec vào Bảng so sánh hoặc đưa số liệu thực nghiệm cụ thể (ví dụ: Accuracy của Word2Vec là bao nhiêu %) để tăng tính thuyết phục khoa học.

---

### 5. Cải thiện Chất lượng Trình bày Đồ họa (Hình 2 & Hình 3)
* **Hình 2 (Bar Chart):** Chưa có thanh sai số (*error bars*), trong khi quy định của Discover yêu cầu rõ phải thể hiện độ phân tán thống kê.
* **Hình 3 (Confusion Matrix):** Trục hoành và trục tung đang để giá trị liên tục mặc định của thư viện matplotlib (`-0.50`, `0.00`, `0.50`, `1.00`, `1.50`) thay vì gắn nhãn phân loại rõ ràng (`High Overload`, `Low/Moderate`).