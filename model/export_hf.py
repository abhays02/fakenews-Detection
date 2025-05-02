from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast

def export_to_hf(model_dir, export_dir, model_name="distilbert-base-uncased"):
    model = DistilBertForSequenceClassification.from_pretrained(model_dir)
    tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)
    model.save_pretrained(export_dir)
    tokenizer.save_pretrained(export_dir)
    print(f"Model and tokenizer exported to {export_dir}")

if __name__ == "__main__":
    import sys
    model_dir = sys.argv[1] if len(sys.argv) > 1 else "../results"
    export_dir = sys.argv[2] if len(sys.argv) > 2 else "./exported_model"
    export_to_hf(model_dir, export_dir)
