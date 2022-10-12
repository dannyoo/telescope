
# Telescope 🔭

## Get Started
```bash
$ pip install -r requirements.txt
$ streamlit run main.py
```

## Inspiration

Providers may have a difficult time understanding the needs of their growing number of patients. I wanted to help providers obtain big-picture insights from their latest unstructured medical notes.

What if providers are able to gain insight to meet the need and educate their community?

## What it does

Telescope is a web app that can be run locally. It provides a near-term forecast of procedures for patients by using their latest unstructured patient visit summaries. First, it shows a table of the predicted future procedures of their aggregated patients. This table shows the aggregated count of each procedure and its average cost. Below, it shows the total future procedures, total cost, and average cost per person. Underneath those metrics, Telescope also includes visualizations to provide more insight into the data with a histogram and a pie chart. The histogram shows the distribution of future procedure costs. The pie chart shows the distribution of future procedures. 

## How I built it

I used the streamlit framework to rapidly prototype a web interface. 

To get the near-term future from the unstructured patient visit summaries, I used “roberta base squad2” NLP architecture trained on the “deepset” dataset with the “huggingface” library.  It is tuned for Question-Answering. Given each summary, the model outputs the answer to the question “What will the people need to do or get in the future?”. 

Since the output could be anything not medically related, I used AWS Comprehend Medical named entity recognition (NER) to identify the procedures in each response from the QA-NLP model.

After getting the data from these, I clean it up into a pandas dataframe that could be useful for the visualizations and insight displayed on the web app interface. 

## Challenges I ran into

Since there is no free apis to get pricing for procedures in the provider’s community, I used dummy data for the pricing of procedures.

## What I learned

- AWS Comprehend Medical
- Plotly for interactive visualizations

## What's next for Telescope

I’m proud of making something interesting that could help providers better serve their community. 

If this does get funded, the next step would be to integrate with medical procedure pricing api’s so that we can get the expected cost of each procedure in any given zip code with up-to-date data.