import pandas as pd
def convert_qa_format(raw_text,out_path):

    # Split the text into individual Q&A lines
    qa_pairs = raw_text.strip().split('\n')
    
    # Process each Q&A pair
    formatted_pairs = []
    for qa in qa_pairs:
        if qa.startswith("Question:"):
            # Extract question and answer
            question = qa[len("Question:"):qa.index("Answer:")].strip()
            answer = qa[qa.index("Answer:") + len("Answer:"):].strip()
            
            # Format according to the desired output
            formatted_pair = f"<s>[INST] {question}[/INST] {answer} </s>"
            formatted_pairs.append(formatted_pair)
    df = pd.DataFrame(formatted_pairs, columns=['text'])
    df.to_csv(out_path, index=False)

# Use the function with the raw text input
# Example usage with a file read
with open('marijuana_nlp.txt', 'r') as file:
    raw_text = file.read()

output_file_path = "fine_tuning.csv"
formatted_text = convert_qa_format(raw_text,output_file_path)


