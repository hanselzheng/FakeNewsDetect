# Scammer Scanner | Fake News Detection Program using Machine Learning

This is a program that uses machine learning to detect fake news articles. The machine uses supervised learning and binary classification to detect fake (1) and real (0) news.

To access the program, run the machine.py file.

To see the accuracy score of the machine, uncomment the three lines at the bottom of the machine.py file:
```bash
   train_accuracy, test_accuracy = train_eval_model()
   print(f"Accuracy Score: {train_accuracy}")
   print(f"Accuracy Score: {test_accuracy}")
```
**🛑 Disclaimer: Checking the accuracy score will take a long time (around 30 - 40 minutes).**


<br>

## How it works
![infograph_h](https://github.com/user-attachments/assets/8c85b508-5165-490f-b5e1-f640941a86db)

<br>

**1. Combine the datasets comprising 10,000 rows of news articles into a single dataset with added labels ("real" or "fake").**

   There are two datasets, one with real articles and the other with fake articles. 
   It is combined into a single dataset, along with the column called "Label" and values of either 1 (fake) or 0 (real).

![FYP Presentation Slides_page-0006](https://github.com/user-attachments/assets/0d2e3c77-1181-4f82-aa81-9bb8972e8075)

<br>

**2. Preprocess the articles by using the stemming process (the process of reducing words into their root words).**
   
   The process starts by initially eliminating non-alphabetic elements such as punctuation, commas, and special characters.
   Next, it will convert the words to lowercase and tokenize them.
   Finally, stop words from the predefined list will be removed, and the remaining words will be rejoined into a single string.
   
![FYP Presentation Slides_page-0007](https://github.com/user-attachments/assets/c7de81a8-a97f-43b7-a524-fd518b6ca618)

<br>

**3. Employ the TF-IDF Vectorizer and Logistic Regression algorithm to assess the significance of words within the corpus.**

   In machine learning, binary classification is a subset of supervised learning algorithm that categorizes observations into one of two classes.
   This function serves as the core process for training the machine and making predictions, deciding whether the news article is reliable or not.
   These algorithms are stored in a pipeline for convenient future access. 

![FYP Presentation Slides_page-0008](https://github.com/user-attachments/assets/f07e5c2d-1a45-45ad-88f8-9246dacac873)
![FYP Presentation Slides_page-0009](https://github.com/user-attachments/assets/1412831e-6651-4a98-b586-67bba47a15d0)

<br>

**4. The dataset is then divided into training and testing sets for the machine.**

   Utilizing the logistic regression algorithm, the machine trains on 70% of the data, while the remaining 30% is used to test the model.
   This can be used to verify the accuracy percentage of the machine by comparing the results of the data.
   The trained model is saved in a joblib file, enabling the program to quickly call the machine without having to repetitively train and test.

![FYP Presentation Slides_page-0010](https://github.com/user-attachments/assets/719ca4ec-41ba-4b4b-a7db-755efc96df7a)
![FYP Presentation Slides_page-0011](https://github.com/user-attachments/assets/c1e5880b-3fc9-4be9-b83f-308cbe23afc1)





   
