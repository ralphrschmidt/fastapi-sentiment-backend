from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import os

# Get the absolute path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Load model and tokenizer using explicit paths
model = AutoModelForSequenceClassification.from_pretrained(
    pretrained_model_name_or_path=BASE_DIR + "/model",  # Load from model folder
    state_dict=None,  # Required when using SafeTensors directly
    trust_remote_code=True  # Allows loading SafeTensors safely
)

tokenizer = AutoTokenizer.from_pretrained(
    pretrained_model_name_or_path=BASE_DIR + "/model"
)

# Create the text classification pipeline explicitly
classifier = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer
)
