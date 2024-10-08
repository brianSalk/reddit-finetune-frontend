# reddit-finetune-frontend
Use content from reddit to finetune an openai model such as davinci.  Link to app [here](https://reddit-finetune.streamlit.app/)
## create_jsonl.py
Gathers data from Reddit and creates a valid JSONL file for fine tuning.  This script uses the title of a submission as the "prompt" and uses the submission body and/or comments as the completion.  [This](https://platform.openai.com/docs/guides/fine-tuning/) website walks you through the fine-tuning steps.  When you get to the part where you need to actually fine-tune the model with a JSONL file, this script will take the data off Reddit and create a valid JSONL file for you using the reddit data of your choice.  Please note that you should still vet the resulting file manually to make sure that the data makes sense.
## app.py
streamlit app that contains the very basic front-end.
## contributing:
To test make changes and test them locally, you must make sure **streamlit** is installed:
```
pip install streamlit
```
then you can test your changes to `app.py` or any other streamlit app locally by running:  
```
streamlit run app.py
```
All contributions are greatly appreciated.  Feel free to open a pull request or an issue to request a feature.  Also if anyone has any kind of front-end knowlege and would like to make this project easier and more pleasant to use that would be double appreciated.
