# ♊ 🏆 Gemini Hackathon
---
## Idea 1


### Overview
Using Gemini as a agent for prompt engineering smaller models using trulens to verify the output

### Problem Statement
There are many benefits in hosting a private model. However, it is difficult and time consumming 
to adjust the behavior of model to get the same results of a larger model.

### Inputs

- Smaller large language model -> Type: LLM
- Agent model (Gemini) -> Type: LLM
- queries -> List[str]
- Prompt Templates (will be a list to sample template fragments) -> List[str]

### Outputs
- metrics -> List[float] (for every element in query)
- New Prompt Templates List[str] | str

---
## Idea 2

Creating an application where a user can input:
 - a receipt from a store and it generates:
- a picture of item(s)
    - using the multimodal capabilities to find item

- the ingredients in the food items
- informs the user if any of the food items contain unhealth ingredients
   - suggests healthier alternatives
- suggests recipes based on the receipt
   - calculates the nutrition per serving of suggested recipe
