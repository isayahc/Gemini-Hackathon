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

### Overview
An AI asistant that helps you buy cost efficieve items at the grocery store while helping avoid harmful products

### Problem Statement
When shopping for food it is always difficult to determine what items contain harmful products. In addition 
it could time consuming to determine what recipes you can make with items you don't often purchase.

### Inputs
- a receipt from a store -> Type: Bytes
- a picture of item(s) -> Type: Bytes
    - using the multimodal capabilities to find item

### Outputs
- the ingredients in the food item(s)
- informs the user if any of the food items contain unhealth ingredients
   - suggests healthier alternatives
- suggests recipes based on input
   - calculates the nutrition per serving of suggested recipe
