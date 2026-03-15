from datasets import Dataset
from sentence_transformers import (
    SentenceTransformer, 
    SentenceTransformerTrainer, 
    losses, 
    SentenceTransformerTrainingArguments
    )
from sentence_transformers.training_args import BatchSamplers
import json
import os 
from torch.utils.data import DataLoader

#meu modelo pré treinado vai ser BERTimbau
model_name = 'neuralmind/bert-base-portuguese-cased'
model = SentenceTransformer(model_name)

#arquivo com meus dados
base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, "scielo.json")

with open(json_path, "r", encoding="utf-8") as f:
    file = json.load(f)

#dataset 
train_dataset = []
train_data_dict = {
    "anchor": [item['Título'] for item in file],
    "positive": [item['resumo'] for item in file]
}
  
train_dataset = Dataset.from_dict(train_data_dict)

#função de perda
#https://sbert.net/docs/sentence_transformer/training_overview.html
#https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss 

loss =  losses.MultipleNegativesRankingLoss(model)

#treinamento 
#https://sbert.net/docs/sentence_transformer/training_overview.html
# 5. (Optional) Specify training arguments

args = SentenceTransformerTrainingArguments(
    # Required parameter:
    output_dir='bertimbau_tuned_scielo',
    # Optional training parameters:
    num_train_epochs=2,
    per_device_train_batch_size=11,
    per_device_eval_batch_size=11,
    learning_rate=2e-5,
    warmup_steps=0.1,
    fp16=False,  # Set to False if you get an error that your GPU can't run on FP16
    bf16=False,  # Set to True if you have a GPU that supports BF16
    batch_sampler=BatchSamplers.NO_DUPLICATES,  # MultipleNegativesRankingLoss benefits from no duplicate samples in a batch
    # Optional tracking/debugging parameters:
    save_total_limit=2,
    logging_steps=50,
)

# 7. Create a trainer & train
trainer = SentenceTransformerTrainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    #eval_dataset=eval_dataset,
    loss=loss,
    #evaluator=dev_evaluator,
)
trainer.train()

#save
model.save_pretrained('bertimbau_tuned_scielo_final')
print("Treino concluído e modelo salvo!")