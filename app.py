from flask import Flask, render_template, request, send_file, jsonify
from scripts.utils import load_spacy_model, highlight_entities
import pandas as pd
from io import BytesIO
import base64

model_name = "en_core_web_sm"
nlp = load_spacy_model(model_name)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # input_text = request.json['input_text']

        if 'input_text' in request.form:
            input_text = request.form['input_text']
        elif 'file' in request.files:
            text_file = request.files['file']
            input_text = text_file.read().decode('utf-8')
        else:
            return jsonify({"error": "No input provided"})

        # Perform Named Entity Recognition
        doc = nlp(input_text)

        # Extract entities
        entities = set([(ent.text, ent.label_) for ent in doc.ents])

        # Generate DataFrame for named entities
        entities_df = pd.DataFrame(entities, columns=["Entity", "Label"])

        # Create download link for entity table CSV file
        csv_buffer = BytesIO()
        entities_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        # print(highlight_entities(input_text, entities))

        # Save the DataFrame to CSV in memory
        return jsonify({
            "output_text": highlight_entities(input_text, entities),
            "download_link": "data:text/csv;base64," + base64.b64encode(csv_buffer.getvalue()).decode()
        })

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
