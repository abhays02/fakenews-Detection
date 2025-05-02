import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

def prepare_news_dataset():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    news_dataset_path = os.path.join(base_dir, 'news_dataset.csv')
    fake_path = os.path.join(base_dir, 'Fake.csv')
    true_path = os.path.join(base_dir, 'True.csv')
    if os.path.exists(news_dataset_path):
        print('news_dataset.csv found. Using it for training.')
        return pd.read_csv(news_dataset_path)
    elif os.path.exists(fake_path) and os.path.exists(true_path):
        print('Fake.csv and True.csv found. Combining them...')
        fake = pd.read_csv(fake_path)
        true = pd.read_csv(true_path)
        fake['label'] = 1
        true['label'] = 0
        if 'text' in fake.columns:
            fake_news = fake[['text', 'label']]
            true_news = true[['text', 'label']]
        else:
            fake_news = fake[['title', 'label']].rename(columns={'title': 'text'})
            true_news = true[['title', 'label']].rename(columns={'title': 'text'})
        df = pd.concat([fake_news, true_news], ignore_index=True)
        df.to_csv(news_dataset_path, index=False)
        print('news_dataset.csv created!')
        return df
    else:
        raise FileNotFoundError('news_dataset.csv or both Fake.csv and True.csv are required.')

def main():
    try:
        df = prepare_news_dataset()
        texts = df['text'].astype(str).tolist()
        labels = df['label'].tolist()
        train_texts, val_texts, train_labels, val_labels = train_test_split(
            texts, labels, test_size=0.2, random_state=42
        )

        print('Vectorizing text...')
        vectorizer = TfidfVectorizer(max_features=10000)
        X_train = vectorizer.fit_transform(train_texts)
        X_val = vectorizer.transform(val_texts)

        print('Training Logistic Regression...')
        clf = LogisticRegression(max_iter=200)
        clf.fit(X_train, train_labels)

        print('Evaluating...')
        preds = clf.predict(X_val)
        acc = accuracy_score(val_labels, preds)
        print(f'Validation Accuracy: {acc:.4f}')
        print(classification_report(val_labels, preds))

        # Save model and vectorizer
        results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
        os.makedirs(results_dir, exist_ok=True)
        joblib.dump(clf, os.path.join(results_dir, 'logreg_model.joblib'))
        joblib.dump(vectorizer, os.path.join(results_dir, 'vectorizer.joblib'))
        print('Model and vectorizer saved to ./results.')
    except Exception as e:
        print(f"Error during training or saving: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
