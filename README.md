# ismakova_project
Приложение состоит из 3-х блоков:
1. Sentiment Analysis (textbox)
2. Sentiment Analysis (file)
3. Statistics 

##Sentiment Analysis (textbox)
Этот блок предназначен для ввода текста через textbox. После нажатия на кнопку 'Do sentiment analysis' выводятся предложения с сформированными тегами, а также итоговую оценку текста.
Запсиь происходит в основной файл: doc2.csv
##Sentiment Analysis (file)
После нажатия на кнопку 'Select file' появляется диалоговое окно с выбором файла (.txt, .csv, .tsv)
- Расширение .txt работает с простым текстом и записывает его в основной файл: doc2.csv
- Расширение .csv/.tsv получает датасет, обрабоатывает все файлы сразу с подсчетом метрик для проверки.
- Формат датасета для csv: id,sentiment,review
- Формат датасета для tsv: id(здесь \t)sentiment(здесь \t)review

##Statistics 
Таблица с посчитанными TF,FP, TN, FN, Precision_t (для позитивных), Recall_t (для позитивных)
F1_T, Precision_f (для негативных), Recall_f(для негативных), F1_N
