from flask import Flask, request, render_template
from flair.data import Sentence
from flair.nn import Classifier
from flair.splitter import SegtokSentenceSplitter


app = Flask(__name__)

splitter = SegtokSentenceSplitter()

# load the DE-NER tagger (-large is also available)
tagger = Classifier.load('de-ner')


def anonymize_text(data):
    # Use splitter to split text into list of sentences
    sentences = splitter.split(data)

    # run DE-NER over sentence
    tagger.predict(sentences)

    for sentence in sentences:
        # Sort entities in reverse order by start position to avoid indexing issues during replacement
        entities = sorted(sentence.get_spans('ner'),
                          key=lambda e: e.start_position, reverse=True)

        # Replace each entity in the sentence with its entity type
        for entity in entities:
            entity_text = entity.text
            entity_type = entity.tag
            start = entity.start_position + 1
            end = entity.end_position
            # Adjusting for the offset caused by previous replacements
            sentence_text = sentence.to_plain_string()
            # if entity_type == 'PER':
            updated_text = sentence_text[:start] + \
                f'<{entity_type}>' + sentence_text[end:]
            # Update the sentence text
            sentence.tokens = Sentence(updated_text).tokens

    # Reconstruct the text from the processed sentences
    processed_text = ' '.join(sentence.to_plain_string()
                              for sentence in sentences)
    return processed_text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/anonymize', methods=['POST'])
def anonymize():
    data = request.get_data().decode('utf-8')
    if len(data) > 4096:
        return "Fehler: Text ist zu lang ({} von {} Zeichen).".format(len(data), 4096)
    return anonymize_text(data)


if __name__ == '__main__':
    app.run(debug=True)
