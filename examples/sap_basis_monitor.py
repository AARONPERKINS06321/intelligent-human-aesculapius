"""Simple SAP Basis monitoring demo using naive Bayes text classification."""

from collections import Counter, defaultdict
import math
import argparse

TRAINING_DATA = [
    ("Work process restart completed successfully", "INFO"),
    ("Database connection lost", "ERROR"),
    ("Background job ended with warnings", "WARNING"),
    ("Kernel fault - memory allocation error", "ERROR"),
    ("User login successful", "INFO"),
    ("System log full", "ERROR"),
    ("Dispatcher running", "INFO"),
    ("Update failed due to lock", "ERROR"),
]

class NaiveBayes:
    def __init__(self):
        self.class_counts = Counter()
        self.word_counts = defaultdict(Counter)
        self.vocab = set()
        self.total_docs = 0

    def train(self, data):
        for text, label in data:
            self.class_counts[label] += 1
            for word in text.lower().split():
                self.word_counts[label][word] += 1
                self.vocab.add(word)
        self.total_docs = sum(self.class_counts.values())

    def predict(self, text):
        words = text.lower().split()
        best_label = None
        best_score = -float("inf")
        for label in self.class_counts:
            log_prob = math.log(self.class_counts[label] / self.total_docs)
            total_words = sum(self.word_counts[label].values())
            for word in words:
                log_prob += math.log(
                    (self.word_counts[label][word] + 1)
                    / (total_words + len(self.vocab))
                )
            if log_prob > best_score:
                best_score = log_prob
                best_label = label
        return best_label


def classify_logs(log_lines):
    nb = NaiveBayes()
    nb.train(TRAINING_DATA)
    results = []
    for line in log_lines:
        label = nb.predict(line)
        results.append((line.strip(), label))
    return results


def main():
    parser = argparse.ArgumentParser(description="Classify SAP log lines")
    parser.add_argument(
        "logfile", nargs="?", default="sap_sample_log.txt", help="Path to log file"
    )
    args = parser.parse_args()

    with open(args.logfile, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line, label in classify_logs(lines):
        print(f"{label}: {line}")


if __name__ == "__main__":
    main()
